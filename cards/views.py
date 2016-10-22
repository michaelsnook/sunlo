from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Card, Deck, Language, Person, CardTranslation

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login')
            return redirect(settings.LOGIN_URL)
    else:
        return render(request, 'cards/login.html')

def logout_page(request):
    logout(request)
    messages.success(request, 'Logged out')
    return redirect(settings.LOGIN_URL)

def card_detail(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    context = {
        'card': card,
    }
    return render(request, 'cards/card_detail.html', context)

def language_detail(request, language_id):
    language = get_object_or_404(Language, pk=language_id)
    context = {
        'language': language,
    }
    return render(request, 'cards/language_detail.html', context)

@login_required
def home(request):
    context = { 'person' : request.user.person, }
    return render(request, 'cards/home.html', context)

@login_required
def deck_detail(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id, person=request.user.person)
    context = {
        'deck': deck,
    }
    return render(request, 'cards/deck_detail.html', context)


@login_required
def deck_add(request):

    if request.method == 'POST':
        language_name = request.POST['language_name']
        language = get_object_or_404(Language, name__iexact=language_name)
        deck = None

        try:
            deck = Deck.objects.get(
                person_id=request.user.person.id,
                language__name__iexact=language_name,
            )
        except ObjectDoesNotExist:
            # TODO: make this create statement work
            deck = Deck.objects.create(person=request.user.person, language=language, )
            if deck is not None:
                messages.success(request, 'Successfully created your new deck!')
                return redirect('/deck/%s' % deck.language.name )
        return redirect('/deck/%s' % deck.language.name )

    if request.method == 'GET':
        context = {
            'languages': Language.objects.all(),
        }
        return render(request, 'cards/deck_add.html', context)


@login_required
def card_add(request):
    person = request.user.person
    context = {
        'person': request.user.person,
        'languages': Language.objects.all(),
    }
    return render(request, 'cards/card_add.html', context)

@login_required
def my_deck(request, deck_language_name):
    person = request.user.person
    deck = get_object_or_404(Deck, language__name__iexact=deck_language_name, person=person)

    context = {
        'person': request.user.person,
        'language': deck.language,
        'deck': deck,
    }
    try:
        context['deck'] = Deck.objects.get(person_id=person.id, language__name__iexact=deck_language_name)
    except ObjectDoesNotExist:
        return render(request, 'cards/deck_not_learning_detail.html', context)


    return render(request, 'cards/deck_detail.html', context)


@login_required
def index(request):
    # show user's own decks. if the user is staff, show all decks
    user = request.user
    if user.is_staff and user.is_active:
        decks = Deck.objects.all()
        people = Person.objects.all()
    else:
        decks = Deck.objects.filter(person=user.person)
        #@TODO add friendships, m2m field on Person
        people = (user.person,) # should be their friends

    context = {
        'decks': decks,
        'people': people,
        'languages': Language.objects.all(),
        'cards': Card.objects.all(),
    }
    return render(request, 'cards/index.html', context)
