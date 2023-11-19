from django.urls import path, re_path

from sites.views import create_site, my_sites_view, my_proxy_view

urlpatterns = [
    path('create_site/', create_site, name='create_site'),
    path('sites/', my_sites_view, name='my_sites'),
    # path('<str:site_name>/', TestProxyView.as_view(), name='proxy_view')
    path('<str:site_name>/', my_proxy_view, name='proxy_view'),
    re_path(r'^(?P<site_name>[^/]+)/(?P<link>.*)$', my_proxy_view, name='my_proxy_view'),
]

app_name = "sites"
