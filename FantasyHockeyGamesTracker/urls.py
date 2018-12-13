from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('TeamList.urls', namespace='team_list')),
    url(r'^admin/', admin.site.urls),
    url(r'^scraper/', include('Scraper.urls', namespace='scraper')),
]
