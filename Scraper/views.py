from django.conf import settings
from django.http import HttpResponse
from Scraper.models import FantasyTeam, NHLTeam, Player, Position
import requests


def scrape_players_for_team(request, team_id):
    def get_players_from_espn_response(json):
        def get_player_from_espn_blob(blob):
            return {
                "name": blob["playerPoolEntry"]['player']['fullName'],
                "espn_nhl_team_id": int(blob["playerPoolEntry"]['player']['proTeamId']),
                "espn_position_id": int(blob['lineupSlotId']),
            }

        roster = json["teams"][0]["roster"]["entries"]
        return [get_player_from_espn_blob(blob) for blob in roster]

    def update_player_in_database(scraped_player, fantasy_team):
        nhl_team = NHLTeam.objects.get(espn_team_id=scraped_player['espn_nhl_team_id'])
        try:
            current_position = Position.objects.get(espn_position_id=scraped_player["espn_position_id"])
            Player.objects.update_or_create(
                name=scraped_player["name"],
                nhl_team=nhl_team,
                defaults={"fantasy_team": fantasy_team, "current_position": current_position}
            )
        except Position.DoesNotExist:
            Player.objects.filter(name=scraped_player["name"], nhl_team=nhl_team).delete()

    target_url = settings.CLUBHOUSE_URL.format(team_id=team_id)
    response_dict = requests.get(target_url).json()
    players = get_players_from_espn_response(response_dict)
    team = FantasyTeam.objects.get(team_id=team_id)
    for player in players:
        update_player_in_database(player, team)

    return HttpResponse(status=200)
