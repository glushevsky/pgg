# Generated by Django 2.1.7 on 2019-04-10 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20190324_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='cover',
            field=models.CharField(blank=True, max_length=6000, null=True),
        ),
    ]
