import base64
import logging
import requests
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.filters import BaseFilterBackend
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication
from django.conf import settings

from .mixins import BulkCreateModelMixin
from .models import Product, Link, ProductType, MapSubcategory, FAQContent, Currency, Wishlist
from .serializers import ProductSerializer, ProductTypeSerializer, LinksSerializer, ProductCreateSerializer, \
    MapSubcategoriesSerializer, FAQContentSerializer, WishListSerializer,UserSerializer

logger = logging.getLogger(__name__)

CURRENCY_API_KEY = settings.CURRENCY_API_KEY


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


map_groups = {
    "tops": ["polos", "t-shirts", "long-sleeves", "tank-tops"],
    "sweatshirts": ["cardigans", "crewnecks", "Hoodies-and-Zipups", "sweatshirts", "turtlenecks"],
    "outerwear": ["bombers", "jackets", "coats", "vests"],
    "bottoms": ["pants", "trousers", "sweatpants", "joggers", "jeans", "shorts"],
    "formal_wear": ["dress-shirt", "dress-pants", "suits", "blazers", "formal-wear"],
    "shoes": ["sneakers", "loafers"],
    "accessories": ["belts", "hats", "gloves", "jewelry", "gloves", "scarves", "backpacks", "socks", "wallets", "other",
                    "eyewear"],
    "underwear": ["bras", "briefs", "corsets-and-bodysuits", "thong"]
}


class BasicAuthPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        token_type, _, credentials = auth_header.partition(' ')

        username, password = base64.b64decode(credentials).decode().split(':')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return False

        password_valid = user.check_password(password)

        if token_type != 'Basic' or not password_valid:
            return False
        return True


class ProductTypeFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        product_type = request.GET.get("product_type")
        subcategory = request.GET.get("subcategory")
        if subcategory:
            return queryset.filter(category__name=subcategory.lower())

        if product_type:
            try:
                product_type = ProductType.objects.get(
                    name=product_type.lower())
            except ProductType.DoesNotExist:
                product_type = None
            if product_type:
                return queryset.filter(category__big_type__name=product_type.name)
        return queryset


class ProductsView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, ProductTypeFilterBackend)
    filter_fields = ('shop_name', 'link__sex')
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ShopView(APIView):

    def get(self, request, *args, **kwargs):
        # parse.delay()
        data = [{"shop_name": shop, "verbose_name": verbose}
                for shop, verbose in Link.SHOP_NAME]
        categories = ProductTypeSerializer(ProductType.objects, many=True).data
        return Response({"shops": data, "categories": categories})


class CategoriesView(ListAPIView):
    queryset = ProductType.objects
    serializer_class = ProductTypeSerializer


class LinksView(ListAPIView):
    queryset = Link.objects
    serializer_class = LinksSerializer
    permission_classes = (BasicAuthPermission,)


class ProductCreateView(ModelViewSet, BulkCreateModelMixin):
    serializer_class = ProductCreateSerializer
    permission_classes = (BasicAuthPermission,)

    def post(self, request, *args, **kwargs):
        links = {el["link"] for el in request.data}
        items_id = list(Product.objects.filter(
            link_id__in=links).values_list("pk", flat=True))
        with atomic():
            response = self.create(request, *args, **kwargs)
        Product.objects.filter(pk__in=items_id).delete()
        return response


class MapSubcategoriesView(ListAPIView):
    queryset = MapSubcategory.objects
    serializer_class = MapSubcategoriesSerializer
    permission_classes = (BasicAuthPermission,)


class FAQContentView(ListAPIView):
    queryset = FAQContent.objects
    serializer_class = FAQContentSerializer


class CurrencyView(APIView):

    def update_currency(self, currency):
        converter = "{}_{}".format(
            currency.currency_from, currency.currency_to)
        url = "http://free.currencyconverterapi.com/api/v5/convert?q={}_{}&compact=y&apiKey={}".format(
            currency.currency_from,
            currency.currency_to,
            CURRENCY_API_KEY
        )
        response = requests.get(url)
        value = response.json().get(converter).get("val")
        currency.value = value
        currency.save()
        logger.info(f"Currency for {converter} updated")
        return currency

    def get(self, request, **kwargs):
        currency_from, currency_to = request.GET.get(
            "from"), request.GET.get("to")

        if not currency_from or not currency_to:
            return Response({"message": "currency_from and currency_to are required arguments"}, status=status.HTTP_400_BAD_REQUEST)
        currency = get_object_or_404(
            Currency, currency_from=currency_from, currency_to=currency_to)

        if not currency.timestamp or currency.timestamp + timezone.timedelta(hours=1) < timezone.now():
            currency = self.update_currency(currency)

        return Response({"value": currency.value}, status=status.HTTP_200_OK)



class WishlistViewSet(ModelViewSet):
    serializer_class = WishListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):  # get the queryset
        return Wishlist.objects.filter(user=self.request.user)


    def create(self, request, *args, **kwargs):
        product_id = request.data.get('productid')

        if not Wishlist.objects.filter(user=self.request.user,product_id=product_id).exists():
            Wishlist.objects.create(user=request.user,product_id=product_id).save()
        else:
            Wishlist.objects.filter(user=self.request.user,product_id=product_id).delete()

        data = Wishlist.objects.filter(user=self.request.user)
        serialize  = WishListSerializer(data,many=True)
        return Response(serialize.data)



class UserCreationSet(ModelViewSet):
    serializer_class = UserSerializer


    def create(self, request, *args, **kwargs):

        username = request.data['username']
        try:
            first_name , last_name = request.data['first_name'].split(' ')
        except:
            first_name = request.data['first_name']
            last_name = ''

        email = request.data['email']
        password = request.data['password']

        if username and User.objects.filter(username=username).exists():
            return Response({"error":'username'})

        if email and User.objects.filter(email=email).exists():
            return Response({"error":'email'})
        else:
            user_obj = User.objects.create(username=username,first_name=first_name,
                                           last_name=last_name,email=email)
            user_obj.set_password(password)
            user_obj.save()
            return Response({"success":True})
