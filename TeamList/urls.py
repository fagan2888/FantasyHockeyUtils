from django.conf.urls import url

from . import views

app_name = "TeamList"
urlpatterns = [
    url(r'^', views.view_fantasy_teams, name='view_fantasy_teams'),
]
