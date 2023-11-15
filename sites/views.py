import requests
from django.http import HttpResponse
from django.shortcuts import render

from .forms import SiteForm
from .models import Site
from django.contrib.auth.decorators import login_required


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


def proxy_view(request, site_name):
    user_site = Site.objects.get(name=site_name, user=request.user)
    # response = requests.get(f'{user_site.url}/{path}')
    response = requests.get(url=user_site.url)
    # response.url = "localhost:8050/profile/"
    # Modify the response content here to replace all link attributes with your internal routing
    # This part of the implementation is complex and depends on the specifics of how you want to handle the proxying.
    return HttpResponse(response)


@login_required
def my_sites_view(request):
    sites = Site.objects.filter(user=request.user)
    site_names = [site.name for site in sites]
    return render(request, 'sites/my_sites.html', {'sites': site_names})
