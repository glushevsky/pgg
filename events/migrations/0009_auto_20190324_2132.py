# Generated by Django 2.1.7 on 2019-03-24 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_event_repeatable'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='average_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='played_player1',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='played_player2',
            field=models.BooleanField(default=False),
        ),
    ]
