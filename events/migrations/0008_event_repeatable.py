# Generated by Django 2.1.7 on 2019-03-24 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20190324_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='repeatable',
            field=models.BooleanField(default=True),
        ),
    ]
