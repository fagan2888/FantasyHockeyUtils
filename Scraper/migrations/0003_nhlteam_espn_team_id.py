# Generated by Django 2.1.1 on 2018-12-11 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scraper', '0002_fantasyteam_team_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='nhlteam',
            name='espn_team_id',
            field=models.IntegerField(default=0),
        ),
    ]
