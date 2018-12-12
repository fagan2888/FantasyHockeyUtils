from django.conf.urls import url

from . import views

app_name = "Scraper"
urlpatterns = [
    url(r'^scrape_players/(?P<team_id>[0-9]*)/$', views.scrape_players_for_team, name='scrape_players'),
    url(r'^scrape_fantasy_teams/$', views.scrape_games_played_for_fantasy_teams, name='scrape_fantasy_teams'),
    url(r'^scrape_nhl_teams/$', views.scrape_games_played_for_nhl_teams, name='scrape_nhl_teams'),
]
