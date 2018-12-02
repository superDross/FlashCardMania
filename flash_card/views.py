from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest

from .forms import CategoryForm, CardCreationForm, CardViewForm
from .qs2table import result_as_table
from .models import FlashCard, Category, GameInstance

import random


def index(request):
    return render(request=request,
                  template_name='flash_card/index.html')


@login_required
def profile_page(request):
    ''' Detailed view of a users Profile.'''
    return render(request=request,
                  template_name='flash_card/profile_page.html',
                  context={'user': request.user})


def card_filtering(request):
    ''' Filter cards based upon form and return cards.'''
    form = CardViewForm(request.POST)
    if form.is_valid():
        category = form.cleaned_data['category']
        level = form.cleaned_data['level']
        users = form.cleaned_data['users']
        card_type = form.cleaned_data['type']
        cards = FlashCard.objects.filter(category__name__in=category,
                                         level__in=level,
                                         created_by__username__in=users,
                                         type__in=card_type)
        return cards


def card_view_selection(request):
    ''' Produces a card table based off of user
        inputted filtering criteria.
    '''
    if request.method == 'POST':
        cards = card_filtering(request)
        columns = ['id', 'question', 'answer', 'level', 'type']
        table = result_as_table(cards, fieldnames=columns)
        return render(request=request,
                      template_name='flash_card/card_list.html',
                      context={'table': table})
    else:
        return render(request=request,
                      template_name='flash_card/generic_form.html',
                      context={'form': CardViewForm(),
                               'title': 'Card Selection'})


def view_all_cards(request):
    ''' Produces a table of all cards in the database.'''
    all_cards = FlashCard.objects.all()
    columns = ['id', 'question', 'answer', 'level', 'type']
    table = result_as_table(all_cards, fieldnames=columns)
    return render(request=request,
                  template_name='flash_card/card_list.html',
                  context={'table': table})


def card_view(request, pk):
    ''' A detailed view of a card.'''
    card = FlashCard.objects.get(pk=pk)
    return render(request=request,
                  template_name='flash_card/full_card_view.html',
                  context={'card': card})


@login_required
def create_category(request):
    ''' Create a Category model.'''
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if Category.objects.filter(name=name.upper()):
                return render(request=request,
                              template_name='flash_card/result.html',
                              context={'title': 'Failure',
                                       'message': 'Category object already exists.'})
            category = Category(name=name.upper(), created_by=request.user)
            category.save()
            return render(request=request,
                          template_name='flash_card/result.html',
                          context={'title': 'Success',
                                   'message': 'Category created successfully.'})
    else:
        return render(request=request,
                      template_name='flash_card/generic_form.html',
                      context={'form': CategoryForm(),
                               'title': 'Category Creation'})


@login_required
def create_card(request):
    ''' Create a Card model.'''
    if request.method == 'POST':
        form = CardCreationForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.cleaned_data['question']
            answer = form.cleaned_data['answer']
            level = form.cleaned_data['level']
            card_type = form.cleaned_data['type']
            image = form.cleaned_data['image']
            audio = form.cleaned_data['audio']
            category = form.cleaned_data['category']
            card = FlashCard(question=question,
                             answer=answer,
                             level=level,
                             type=card_type,
                             image=image,
                             audio=audio,
                             category=category,
                             created_by=request.user)
            card.save()
            return render(request=request,
                          template_name='flash_card/result.html',
                          context={'title': 'Success',
                                   'message': 'Card created successfully.'})
        else:
            return render(request=request,
                          template_name='flash_card/result.html',
                          context={'title': 'Failure',
                                   'message': form.errors})
    else:
        return render(request=request,
                      template_name='flash_card/generic_form.html',
                      context={'form': CardCreationForm(),
                               'title': 'Card Creation'})


# def get_random_cards(cards, num=10):
#     ''' Get 10 or less objects from a Card QuerySet.'''
#     random_cards = []
#     n = num if cards.count() > num else cards.count()
#     for _ in range(n):
#         card = random.choice(cards)
#         random_cards.append(card)
#     return random_cards


@login_required
def create_game(request):
    ''' Game form to select specific cards for game session.'''
    if request.method == 'POST':
        if not request.session.get('cards'):
            cards = card_filtering(request)
        else:
            cards = FlashCard.objects.filter(pk__in=request.session['cards'])
        # add cards pk list value to session
        request.session['cards'] = list(cards.values_list('pk', flat=True))
        return redirect('flash_card:game_card_view')
    else:
        return render(request=request,
                      template_name='flash_card/generic_form.html',
                      context={'form': CardViewForm(),
                               'title': 'Game Card Selection'})


@login_required
def game_view(request):
    ''' View individual cards in game.'''
    cards = request.session['cards']
    if not cards:
        # game completion page
        return render(request=request,
                      template_name='flash_card/result.html',
                      context={'title': 'Game Complete',
                               'message': 'You have exhausted all cards'})
    # get random card pk from cards in session
    card_pk = random.choice(request.session['cards'])
    cards.remove(card_pk)
    request.session['cards'] = cards
    card = FlashCard.objects.get(pk=card_pk)
    return render(request=request,
                  template_name='flash_card/game_card_view.html',
                  context={'card': card})
