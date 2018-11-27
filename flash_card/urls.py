from django.contrib import admin
from django.urls import path, include
from flash_card import views

urlpatterns = [
    path('profile/', views.profile_page, name='profile_page'),
    path('', views.index, name='index'),
    path('create/category/', views.create_category, name='create_category'),
    path('create/card/', views.create_card, name='create_card'),
    path('card/selection/', views.card_view_selection, name='card_selection'),
    path('card/list/', views.view_all_cards, name='card_list'),
    path('card/<int:pk>/', views.card_view, name='card_view'),
    path('game/', views.game_view, name='create_game'),
    path('game/<uuid:game>/', views.play, name='play'),
]
