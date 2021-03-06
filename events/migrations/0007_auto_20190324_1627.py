# Generated by Django 2.1.7 on 2019-03-24 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20190323_1454'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=3000)),
            ],
        ),
        migrations.RenameField(
            model_name='event',
            old_name='visibility',
            new_name='visibility_player1',
        ),
        migrations.AddField(
            model_name='event',
            name='visibility_player2',
            field=models.BooleanField(default=True),
        ),
    ]
