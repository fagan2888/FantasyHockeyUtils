from django.conf.urls import url

from . import views

app_name = "Scraper"
urlpatterns = [
    url(r'^scrape_players/(?P<team_id>[0-9]*)/$', views.scrape_players_for_team, name='scrape_players'),
]
