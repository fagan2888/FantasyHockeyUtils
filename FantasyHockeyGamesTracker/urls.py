from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('TeamList.urls', namespace='team_list')),
    url(r'^admin/', admin.site.urls),
    url(r'^clubhouse/', include('Clubhouse.urls', namespace='clubhouse')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
