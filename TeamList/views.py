from django.http import HttpResponse
from django.template import loader
from django.views.decorators.http import require_http_methods
from Scraper.models import FantasyTeam


def scrape_fantasy_teams_if_necessary():
    pass


@require_http_methods(["GET"])
def view_fantasy_teams(request):
    scrape_fantasy_teams_if_necessary()
    all_teams = sorted(list(FantasyTeam.objects.all()), key=lambda x: x.total_games_played, reverse=True)

    context = {"teams": [(team, i) for i, team in enumerate(all_teams)]}
    template = loader.get_template('TeamList/TeamList.html')

    return HttpResponse(template.render(context, request))
