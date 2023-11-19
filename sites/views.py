from wsgiref.util import is_hop_by_hop

import requests
from django.http import HttpResponse, Http404, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render
from urllib.parse import urljoin, urlparse

from django.views.decorators.csrf import csrf_exempt

from .forms import SiteForm
from .models import Site
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
# from revproxy.views import ProxyView
from proxy.views import proxy_view


def create_site(request):
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            new_site = form.save(commit=False)
            new_site.user = request.user
            new_site.save()
            return render(request, "sites/my_sites.html")  # Redirect to a view that shows a list of user's sites
    else:
        form = SiteForm()
    return render(request, 'sites/create_site.html', {'form': form})

#
# class TestProxyView(ProxyView):
#     upstream = 'https://google.com'


# @login_required
# def my_proxy_view(request, site_name, link=None):
#     try:
#         user_site = Site.objects.get(name=site_name, user=request.user)
#     except Site.DoesNotExist:
#         user_site = None
#     if not user_site:
#         return render(request, 'sites/site_not_exist.html')
#     else:
#         site_url = user_site.url
#         if link:
#             site_url = urljoin(site_url, link)
#         response = requests.get(url=site_url)
#         # Modify the response content here to replace all link attributes with your internal routing
#         # This part of the implementation is complex and depends on the specifics of how you want to handle the proxying.
#         return HttpResponse(response)


@login_required
def my_proxy_view(request, site_name, link=''):
    # Fetch the base URL from the database for the first visit
    try:
        user_site = Site.objects.get(name=site_name, user=request.user)
    except Site.DoesNotExist:
        return render(request, 'sites/site_not_exist.html')
    # Construct the full URL to fetch
    if link:
        # Handle a given path
        parsed_link = urlparse(link)
        if parsed_link.scheme:
            # If link is a full URL, use it as is
            site_url = link
        else:
            # If link is a relative path, construct the full URL
            site_url = urljoin(user_site.url, link.lstrip('/'))
    else:
        # If no specific path is given, use the base URL
        site_url = user_site.url

    # Fetch the content from the external site
    try:
        response = requests.get(site_url)
        response.raise_for_status()  # Raises HTTPError for bad requests (4XX or 5XX)
    except requests.RequestException as e:
        return HttpResponse(f"An error occurred when trying to reach the site: {e}", status=502)
    # If the response is HTML, modify it
    content_type = response.headers.get('Content-Type', '')
    if 'text/html' in content_type:
        soup = BeautifulSoup(response.content, 'html.parser')
        current_site_domain = urlparse(site_url).netloc
        # Rewrite links to go through the proxy
        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            parsed_href = urlparse(href)
            # Check if the href leads to the same domain
            if parsed_href.netloc and parsed_href.netloc != current_site_domain:
                # If the domain is different, do not rewrite the link
                continue
            else:
                # If it's the same domain or a relative URL, rewrite it
                # Remove the domain from absolute URLs, if present
                relative_path = href.replace(parsed_href.scheme + '://' + parsed_href.netloc, '', 1).lstrip('/')
                new_href = request.build_absolute_uri(f'/{site_name}/{relative_path}')
                anchor['href'] = new_href
        return HttpResponse(str(soup), content_type='text/html')
    # If the response is not HTML (like an image or CSS file), return it as-is
    return HttpResponse(response.content, content_type=content_type)


@login_required
def my_sites_view(request):
    sites = Site.objects.filter(user=request.user)
    site_names = [site.name for site in sites]
    return render(request, 'sites/my_sites.html', {'sites': site_names})
