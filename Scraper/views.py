from django.conf import settings
from django.http import HttpResponse
from Scraper.models import FantasyTeam, NHLTeam, Player, Position
import requests


def scrape_games_played_for_fantasy_teams(request):
    def get_teams_from_espn_response(json):
        team_array = json["schedule"][0]["teams"]
        team_array = sorted(team_array, key=lambda x: x["teamId"])
        return [team_blob["cumulativeScore"]["statBySlot"] for team_blob in team_array]

    def update_team_in_database(team_id, team_json):
        team = FantasyTeam.objects.get(team_id=team_id)
        team.games_played_center = int(team_json["0"]["value"])
        team.games_played_left_wing = int(team_json["1"]["value"])
        team.games_played_right_wing = int(team_json["2"]["value"])
        team.games_played_defense = int(team_json["4"]["value"])
        team.games_played_goalie = int(team_json["5"]["value"])
        team.games_played_utility = int(team_json["6"]["value"])
        team.save()

    target_url = settings.ALLOWANCES_URL
    response_dict = requests.get(target_url).json()
    teams = get_teams_from_espn_response(response_dict)
    for i in range(len(teams)):
        update_team_in_database(i + 1, teams[i])

    return HttpResponse(status=200)


def scrape_games_played_for_nhl_teams(request):
    def get_teams_from_nhl_response(json):
        def get_teams_from_division(division_json):
            team_json = division_json['teamRecords']
            teams_in_division = []
            for team_blob in team_json:
                teams_in_division.append({
                    "name": team_blob['team']['shortName'],
                    "games_played": int(team_blob['gamesPlayed']),
                })

            return teams_in_division

        divisions = json['records']
        teams_in_league = []
        for division in divisions:
            teams_in_league += get_teams_from_division(division)

        return teams_in_league

    def update_team_in_database(team):
        nhl_team = NHLTeam.objects.get(long_name=team['name'])
        nhl_team.games_played = team['games_played']
        nhl_team.save()

    target_url = settings.STANDINGS_URL
    response_dict = requests.get(target_url).json()
    teams = get_teams_from_nhl_response(response_dict)
    for team in teams:
        update_team_in_database(team)

    return HttpResponse(status=200)


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
