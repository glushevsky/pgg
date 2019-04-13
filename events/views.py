# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Q
from events.models import Event, State, Game, PCGame

# import csv
# import pandas as pd
import random
import json
# import math


# def csv_reader(file_obj):
#     reader = csv.reader(file_obj)
#     for row in reader:
#         print(row)


# def parse_data(data):
#     events = []
#     for category in ['0', '3', '6', '9']:
#         for event in range(len(data[category])):
#             category_name = str(int(category) + 1)
#             category_descr = str(int(category) + 2)
#             number = data[category][event]
#             name = data[category_name][event]
#             description = data[category_descr][event]
#             print(type(number), isinstance(number, str))
#             try:
#                 events.append([int(number), name, description])
#             except:
#                 pass
#     print(len(events))
#     return events


# случайный выбор с обновлением статуса
def randomize(player, events):
    result = random.choice(events)
    del_state(player)
    set_state(player, result['additions'], result['deprecations'])
    result = update_repeat(player, result)
    return result


# получение названия типа
def get_type(num):
    if num == 1:
        return 'Хорошее'
    elif num == 2:
        return 'Плохое'
    else:
        return 'Неизвестное'


# получение название подтипа
def get_subtype(num):
    if num == 1:
        return 'Немедленное событие'
    elif num == 2:
        return 'Событие на игру'
    elif num == 3:
        return 'Событие на этап'
    elif num == 4:
        return 'Абсолютное событие'
    else:
        return 'Неизвестное событие'


# парсинг доп. событий
def parse_special_list(special_data):
    specials = []
    try:
        if special_data is not None:
            for element in special_data.split(','):
                try:
                    specials.append(int(element))
                except:
                    pass
    except:
        pass
    return specials


# формирование списка событий
def get_event_list(player, visible, con_ids, exc_ids):
    event_list = []
    if player == 1:
        events = Event.objects.filter((Q(visibility_player1=visible)|Q(id__in=con_ids))&Q(quantity__gte=1)).exclude(id__in=exc_ids)
    elif player == 2:
        events = Event.objects.filter((Q(visibility_player2=visible) | Q(id__in=con_ids)) & Q(quantity__gte=1)).exclude(id__in=exc_ids)
    for event in events:
        for elem in range(event.quantity):
            event_list.append({
                'id': event.id,
                'type': (event.type, get_type(event.type)),
                'subtype': (event.subtype, get_subtype(event.subtype)),
                'name': event.name,
                'descr': event.descr,
                'additions': parse_special_list(event.connections),
                'deprecations': parse_special_list(event.exceptions),
                'repeat': event.repeatable
            })
    return event_list


# удаление статуса
def del_state(player):
    State.objects.filter(player=player).delete()


# добавление элемента статуса
def set_state_element(player, addition, num):
    try:
        event = Event.objects.get(id=num)
        State(player=player, addition=addition, element=event).save()
    except:
        pass


# добавление нового статуса
def set_state(player, additions, deprecations):
    for num in additions:
        set_state_element(player, True, num)
    for num in deprecations:
        set_state_element(player, False, num)


# получение сохраненного статуса
def get_state(player):
    additions = []
    deprecations = []
    stats = State.objects.filter(player=player)
    for stat in stats:
        if stat.addition is True:
            additions.append(stat.element.id)
        else:
            deprecations.append(stat.element.id)
    return additions, deprecations


# колесо событий
def start_event_manager(player):
    additions, deprecations = get_state(player)
    events = get_event_list(player, True, additions, deprecations)
    result = randomize(player, events)
    return events, result


def update_repeat(player, result):
    # print('=====>', result['repeat'], player, result['name'])
    if result['repeat'] is False:
        ev = Event.objects.get(name=result['name'])
        # print(ev.id, ev.name)
        if player == 1:
            ev.visibility_player1 = 0
        elif player == 2:
            ev.visibility_player2 = 0
        ev.save()
    return result


def main(request, player):
    # события
    # events, result = start_event_manager(player)
    additions, deprecations = get_state(player)
    events = get_event_list(player, True, additions, deprecations)
    tracks = ['chika_full.mp3', 'password_full.mp3', 'enjoykin.mp3', 'kappa.mp3', 'cat.mp3']
    context = {'player': player,
               'music': random.choice(tracks),
               'events': json.dumps(events)}
    if request.method == 'POST':
        context['environment'] = True
        result = randomize(player, events)
        context['result'] = result
        print(context['music'])
    return render(request, 'events.html', context)


def menu(request):
    return render(request, 'menu.html', {})


def game(request):
    context = {}
    if request.method == 'POST':
        game_set = Game.objects.all()
        games = []
        for game_el in game_set:
            games.append({'name': game_el.name,
                          'time': game_el.average_time,
                          'player1': game_el.played_player1,
                          'player2': game_el.played_player2})
        result = random.choice(games)
        context['games'] = json.dumps(games)
        context['result'] = result
        context['environment'] = True
        tracks = ['chika_full.mp3', 'password_full.mp3', 'enjoykin.mp3', 'kappa.mp3', 'cat.mp3']
        context['music'] = random.choice(tracks)
    return render(request, 'game.html', context)


def progress(request, roll_type=None):
    context = {}
    if roll_type == 1:
        game_set = Game.objects.filter(coop=1)
    elif roll_type == 2:
        game_set = PCGame.objects.all()
    else:
        game_set = Game.objects.all()
    games = []
    for num, game_el in enumerate(game_set):
        cover = 'covers/'
        if game_el.cover:
            cover += game_el.cover
        else:
            cover += 'default.jpg'
        games.append({'label': game_el.name,
                      'value': num,
                      'question': game_el.name,
                      'descr': 'Среднее время прохождения: ' + str(game_el.average_time) + ' ч.',
                      'img': cover
                      })
    random.shuffle(games)
    context['games'] = json.dumps(games)
    tracks = ['chika_full.mp3', 'password_full.mp3', 'enjoykin.mp3', 'kappa.mp3', 'cat.mp3']
    context['music'] = random.choice(tracks)
    return render(request, 'progress.html', context)


def progress_event(request, roll_type=None):
    context = {}
    # if roll_type == 1:
    #     game_set = Game.objects.filter(coop=1)
    # else:
    event_set = Event.objects.all()
    events = []
    for num, event_el in enumerate(event_set):
        # cover = 'covers/'
        # if event_el.cover:
        #     cover += game_el.cover
        # else:
        #     cover += 'default.jpg'
        events.append({'label': event_el.name,
                      'value': num,
                      'question': event_el.descr
                      # 'descr': 'Среднее время прохождения: ' + str(event_el.average_time) + ' ч.',
                      # 'img': cover
                      })
    random.shuffle(events)
    context['events'] = json.dumps(events)
    # tracks = ['chika_full.mp3', 'password_full.mp3', 'enjoykin.mp3', 'kappa.mp3', 'cat.mp3']
    # context['music'] = random.choice(tracks)
    return render(request, 'progress_event.html', context)