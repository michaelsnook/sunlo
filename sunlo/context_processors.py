from cards.models import User, Person, Deck, Language

def app_context(request):
    context = {
        'languages': Language.objects.all(),
        'user_count': Person.objects.count(),
    }
    if request.user.is_authenticated:
        context.update({
            'person': request.user.person,
            'decks': request.user.person.deck_set.all()
        })
    return context
