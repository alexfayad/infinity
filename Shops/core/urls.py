from .views import *
from django.urls import path,include
from django.views.decorators.cache import cache_page
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

#Rest Routes
router = routers.DefaultRouter()

router.register(r'wishlist',WishlistViewSet,base_name='wishlist'),
router.register(r'signup',UserCreationSet,base_name='signup'),


#Django Urls
urlpatterns = [

        path('',include(router.urls)),
        path('product/', cache_page(60 * 5)(ProductsView.as_view())),
        path('shop/', cache_page(60 * 5)(ShopView.as_view())),
        path('categories/', CategoriesView.as_view()),
        path('map_categories/', MapSubcategoriesView.as_view()),
        path('links/', LinksView.as_view()),
        path('parser_data/', ProductCreateView.as_view({'get': 'list'})),
        path('faq/', FAQContentView.as_view()),
        path('currency/', CurrencyView.as_view()),
        path('get_token/', obtain_auth_token, name='api_token_auth'),

    ]
