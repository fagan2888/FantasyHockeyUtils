from django.http import HttpResponse
from django.template import loader
from django.views.decorators.http import require_http_methods
from Scraper.models import Player


def scrape_players_for_team(team_name):
    pass


@require_http_methods(["GET"])
def view_fantasy_teams(request, team_name):
    scrape_players_for_team(team_name)
    players_on_team = list(Player.objects.filter(fantasy_team__name=team_name).order_by('name'))
    context = {
        "players": [(player, i) for i, player in enumerate(players_on_team)],
        "team_name": team_name,
    }
    template = loader.get_template('Clubhouse/Clubhouse.html')

    return HttpResponse(template.render(context, request))
