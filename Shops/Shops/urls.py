from django.contrib import admin
from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView

from core.views import ProductsView, ShopView, CategoriesView, LinksView, ProductCreateView, MapSubcategoriesView, \
    FAQContentView, CurrencyView

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/product/', cache_page(60 * 5)(ProductsView.as_view())),
    # path('api/product/', ProductsView.as_view()),
    path('api/shop/', cache_page(60 * 5)(ShopView.as_view())),
    path('api/categories/', CategoriesView.as_view()),
    path('api/map_categories/', MapSubcategoriesView.as_view()),
    path('api/links/', LinksView.as_view()),
    path('api/parser_data/', ProductCreateView.as_view({'get': 'list'})),
    path('api/faq/', FAQContentView.as_view()),
    path('api/currency/', CurrencyView.as_view()),
]

frontend_patterns = [
    re_path(r'^.*', TemplateView.as_view(template_name="index.html"), name='home'),
]

urlpatterns += frontend_patterns