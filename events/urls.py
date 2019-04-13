from django.urls import path
from events.views import main, menu, game, progress, progress_event

urlpatterns = [
    path('', menu),
    path('<int:player>/', main),
    path('game/', game),
    path('progress/', progress),
    path('progress/<int:roll_type>/', progress),
    path('progress_event/', progress_event)
]