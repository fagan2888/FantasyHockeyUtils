from django.conf import settings
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.http import require_http_methods
from Scraper.models import FantasyTeam, NHLTeam, Player
from Scraper.views import scrape_fantasy_teams_if_necessary, scrape_nhl_teams_if_necessary, scrape_players_for_team


@require_http_methods(["GET"])
def view_team(request, team_id):
    scrape_players_for_team(request, team_id)
    scrape_fantasy_teams_if_necessary(request)
    scrape_nhl_teams_if_necessary(request)

    team = FantasyTeam.objects.get(team_id=team_id)
    players_on_team = list(Player.objects.filter(fantasy_team__name=team.name).order_by('name'))

    centers = [x for x in players_on_team if x.current_position.name == "Center"]
    left_wings = [x for x in players_on_team if x.current_position.name == "Left Wing"]
    right_wings = [x for x in players_on_team if x.current_position.name == "Right Wing"]
    defense = [x for x in players_on_team if x.current_position.name == "Defense"]
    utilities = [x for x in players_on_team if x.current_position.name == "Utility"]
    goalies = [x for x in players_on_team if x.current_position.name == "Goalie"]

    nhl_teams = list(NHLTeam.objects.all())
    nhl_team_dict = {team.espn_team_id: 82 - team.games_played for team in nhl_teams}
    center_gp = sum(
        [nhl_team_dict[center.nhl_team.espn_team_id] for center in centers]
    ) + team.games_played_center - settings.MAX_GP_CENTER
    left_wing_gp = sum(
        [nhl_team_dict[left_wing.nhl_team.espn_team_id] for left_wing in left_wings]
    ) + team.games_played_left_wing - settings.MAX_GP_LEFT_WING
    right_wing_gp = sum(
        [nhl_team_dict[right_wing.nhl_team.espn_team_id] for right_wing in right_wings]
    ) + team.games_played_right_wing - settings.MAX_GP_RIGHT_WING
    defense_gp = sum(
        [nhl_team_dict[defense.nhl_team.espn_team_id] for defense in defense]
    ) + team.games_played_defense - settings.MAX_GP_DEFENSE
    utility_gp = sum(
        [nhl_team_dict[utility.nhl_team.espn_team_id] for utility in utilities]
    ) + team.games_played_utility - settings.MAX_GP_UTILITY
    goalie_gp = round((sum(
        [nhl_team_dict[goalie.nhl_team.espn_team_id] for goalie in goalies]
    ) * 0.75)) + team.games_played_goalie - settings.MAX_GP_GOALIE

    context = {
        "centers": [(player, i) for i, player in enumerate(centers)],
        "left_wings": [(player, i + 3) for i, player in enumerate(left_wings)],
        "right_wings": [(player, i + 6) for i, player in enumerate(right_wings)],
        "defense": [(player, i + 9) for i, player in enumerate(defense)],
        "utilities": [(player, i + 14) for i, player in enumerate(utilities)],
        "goalies": [(player, i + 15) for i, player in enumerate(goalies)],
        "center_gp": center_gp,
        "left_wing_gp": left_wing_gp,
        "right_wing_gp": right_wing_gp,
        "defense_gp": defense_gp,
        "utility_gp": utility_gp,
        "goalie_gp": goalie_gp,
        "team_name": team.name,
    }
    template = loader.get_template('Clubhouse/Clubhouse.html')

    return HttpResponse(template.render(context, request))
