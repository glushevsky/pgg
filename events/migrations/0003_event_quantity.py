# Generated by Django 2.1.7 on 2019-03-23 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_visibility'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
