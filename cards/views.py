from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse


from .models import Card, Deck, Language, Person, CardTranslation

# Create your views here.

def index(request):
    context = {
        'decks': Deck.objects.all(),
        'languages': Language.objects.all(),
        'cards': Card.objects.all(),
    }
    return render(request, 'cards/index.html', context)

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
