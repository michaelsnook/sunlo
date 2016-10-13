from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Card, Deck, Language, Person, CardTranslation

def index(request):
    context = {
        'decks': Deck.objects.all(),
        'languages': Language.objects.all(),
        'cards': Card.objects.all(),
    }
    return render(request, 'cards/index.html', context)

@login_required
def home(request):
    context = { 'person' : request.user.person, }
    return render(request, 'cards/home.html', context)

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

def deck_detail(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    context = {
        'deck': deck,
    }
    return render(request, 'cards/deck_detail.html', context)
