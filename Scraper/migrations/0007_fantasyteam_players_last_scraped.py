# Generated by Django 2.1.1 on 2018-12-23 18:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scraper', '0006_remove_fantasyteam_players_last_scraped'),
    ]

    operations = [
        migrations.AddField(
            model_name='fantasyteam',
            name='players_last_scraped',
            field=models.DateTimeField(default=datetime.datetime(1992, 4, 20, 0, 0)),
        ),
    ]