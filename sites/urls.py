from django.urls import path

from sites.views import create_site, my_sites_view, proxy_view

urlpatterns = [
    # ... other patterns ...
    path('create_site/', create_site, name='create_site'),
    path('<str:site_name>/', proxy_view, name='proxy_view'),
    path('sites/', my_sites_view, name='my_sites')
]

app_name = "sites"
