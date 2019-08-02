from django.contrib import admin
from django.urls import path, re_path,include
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/',include('core.urls')),

]

frontend_patterns = [
    re_path(r'^.*', TemplateView.as_view(template_name="index.html"), name='home'),
]

urlpatterns += frontend_patterns
