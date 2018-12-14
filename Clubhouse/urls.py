from django.conf.urls import url

from . import views

app_name = "Clubhouse"
urlpatterns = [
    url(r'view_team/(?P<team_id>[0-9]*)/$', views.view_team, name='view_team'),
    url(r'refresh_team/(?P<team_id>[0-9]*)/$', views.get_team_refresh, name='refresh_team'),
]
