from django.conf.urls import url

from . import views

app_name = "TeamList"
urlpatterns = [
    url(r'^', views.get_all_fantasy_teams, name='get_fantasy_teams'),
]
