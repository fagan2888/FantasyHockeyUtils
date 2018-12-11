from django.db import models


class FantasyTeam(models.Model):
    name = models.CharField(max_length=50)
    team_id = models.IntegerField(default=0)
    games_played_center = models.IntegerField(default=0)
    games_played_left_wing = models.IntegerField(default=0)
    games_played_right_wing = models.IntegerField(default=0)
    games_played_defense = models.IntegerField(default=0)
    games_played_goalie = models.IntegerField(default=0)
    games_played_utility = models.IntegerField(default=0)


class NHLTeam(models.Model):
    espn_team_id = models.IntegerField(default=0)
    long_name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=3)
    games_played = models.IntegerField(default=0)


class Position(models.Model):
    name = models.CharField(max_length=10)
    espn_position_id = models.IntegerField(default=0)


class Player(models.Model):
    name = models.CharField(max_length=50)
    nhl_team = models.ForeignKey(NHLTeam, on_delete=models.CASCADE, default=None)
    fantasy_team = models.ForeignKey(FantasyTeam, on_delete=models.CASCADE, default=None)
    current_position = models.ForeignKey(Position, on_delete=models.CASCADE, default=None)