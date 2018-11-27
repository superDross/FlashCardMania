from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest

from .forms import CategoryForm, CardCreationForm, CardViewForm, CardQuestionForm
from .qs2table import result_as_table
from .utils import random_card_color
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
    ''' Filter cards based on form and return cards.'''
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
    color = random_card_color()
    style = f'{color};min-width:400px'
    return render(request=request,
                  template_name='flash_card/card_view.html',
                  context={'card': card,
                           'style': style})


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
                      template_name='flash_card/create_form.html',
                      context={'form': CardForm(),
                               'title': 'Card Creation'})


def get_random_cards(cards, num=10):
    ''' Get 10 or less objects from a Card QuerySet.'''
    random_cards = []
    n = num if cards.count() > num else cards.count()
    for _ in range(n):
        card = random.choice(cards)
        random_cards.append(card)
    return random_cards


@login_required
def game_view(request):
    ''' Creates GameInstance based on player input and
        redirects to the game.
    '''
    if request.method == 'POST':
        cards = card_filtering(request)
        cards = get_random_cards(cards)
        game = GameInstance(participant=request.user,
                            type='c',
                            score=0)
        game.save()
        for card in cards:
            game.cards.add(card)
        game.save()
        return HttpResponseRedirect(reverse(f'flash_card:play',
                                            kwargs={'game': game}))

    else:
        return render(request=request,
                      template_name='flash_card/generic_form.html',
                      context={'form': CardViewForm(),
                               'title': 'Card Selection'})


@login_required
def play(request, game, round_number=0):
    card = game.cards.all()[round_number]
    if request.method == 'POST':
        questions = [x.answer for x in get_random_cards(game.cards.all(), 4)]
        form = CardQuestionForm(request.POST, choices=questions)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            if answer == card.answer:
                game.score += 1
            if round_number < game.cards.count():
                round_number += 1
                return HttpResponseRedirect(
                    reverse('flash_card:play', kwargs={'game': game,
                                                       'round_number': round_number})
                )
            else:
                # convert game score to percentage
                game.score = int(game.score / game.cards.count())
                # render score page
                pass

    else:
        return render(request=request,
                      context={'form': CardQuestionForm(),
                               'title': 'Play',
                               'game': game})
