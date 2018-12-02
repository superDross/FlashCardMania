from django.contrib import admin
from django.urls import path, include
from flash_card import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile_page, name='profile_page'),
    path('create/category/', views.create_category, name='create_category'),
    path('create/card/', views.create_card, name='create_card'),
    path('create/game/', views.create_game, name='game_form'),
    path('card/selection/', views.card_view_selection, name='card_selection'),
    path('card/list/', views.view_all_cards, name='card_list'),
    path('card/<int:pk>/', views.card_view, name='card_view'),
    path('game/card/', views.game_view, name='game_card_view'),
]
