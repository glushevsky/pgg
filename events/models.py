# -*- coding: utf-8 -*-
from django.db import models


class Event(models.Model):
    type = models.IntegerField()
    subtype = models.IntegerField()
    name = models.CharField(max_length=3000, default=None, blank=True, null=True)
    descr = models.CharField(max_length=6000, default=None, blank=True, null=True)
    visibility_player1 = models.BooleanField(default=True)
    visibility_player2 = models.BooleanField(default=True)
    quantity = models.IntegerField(default=1)
    connections = models.CharField(max_length=1000, default=None, blank=True, null=True)
    exceptions = models.CharField(max_length=1000, default=None, blank=True, null=True)
    repeatable = models.BooleanField(default=True)


class State(models.Model):
    player = models.IntegerField()
    addition = models.BooleanField()
    element = models.ForeignKey('Event', on_delete=models.PROTECT)

class Game(models.Model):
    name = models.CharField(max_length=3000)
    average_time = models.IntegerField(default=0)
    played_player1 = models.BooleanField(default=False)
    played_player2 = models.BooleanField(default=False)
    ps_plus = models.BooleanField(default=False)
    cover = models.CharField(max_length=6000, blank=True, null=True)
    coop = models.IntegerField(default=0)

class PCGame(models.Model):
    name = models.CharField(max_length=3000)
    average_time = models.IntegerField(default=0)
    played_player1 = models.BooleanField(default=False)
    played_player2 = models.BooleanField(default=False)
    ps_plus = models.BooleanField(default=False)
    cover = models.CharField(max_length=6000, blank=True, null=True)
    coop = models.IntegerField(default=0)