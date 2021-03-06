from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import User, Card, Deck, Language, Person, CardTranslation, DeckMembership

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login')
            return redirect(settings.LOGIN_URL)
    else:
        return render(request, 'cards/login.html', { 'login': 'active' })

def logout_page(request):
    logout(request)
    return redirect('home')

def user_register(request):
    if request.method == 'POST':
        user = User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('password'))
        person = Person.objects.create(user=user)
        if user is not None:
            login(request, user)
            messages.success(request, 'Congratulations on creating your account!')
            return redirect('user_profile')
        else:
            messages.error(request, 'Something went wrong, please try again')
    return render(request, 'cards/login.html', { 'signup': 'active' })

def card_detail(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    deckmembership = {}
    deck = {}
    if request.user.is_authenticated:
        try:
            deckmembership = DeckMembership.objects.get(card=card, deck__person=request.user.person)
        except ObjectDoesNotExist:
            deckmembership = {}
        try:
            deck = Deck.objects.get(language=card.language, person=request.user.person)
        except ObjectDoesNotExist:
            deckmembership = {}

    context = {
        'card': card,
        'deck': deck,
        'membership': deckmembership,
    }
    return render(request, 'cards/card_detail.html', context)

@login_required
def card_membership_update(request, card_id, status):
    card = get_object_or_404(Card, pk=card_id)
    deck = get_object_or_404(Deck, person=request.user.person, language=card.language)
    try:
        deckmembership = DeckMembership.objects.get(card=card, deck=deck)
        deckmembership.status=status
        deckmembership.save()

    except ObjectDoesNotExist:
        deckmembership = DeckMembership.objects.create(
            card=card,
            deck=deck,
            status=status,
        )

    messages.success(request, "Status for card \"%s\" set to \"%s\"" % (card.text,status))

    return (request, deckmembership)

@login_required
def membership_update(request, card_id):
    if request.method == 'GET':
        return redirect('card_detail', card_id)
    if request.method == 'POST':
        request, deckmembership = card_membership_update(request, card_id, request.POST.get('status'))
        context = {
            'card': deckmembership.card or {},
            'membership': deckmembership or {},
            'card_language_matches_a_deck': True,
        }
        return redirect('card_detail', card_id)

@login_required
def browse_deck(request, deck_language_name):
    person = request.user.person
    deckmembership = {}
    try:
        deck = Deck.objects.get(person=person, language__name__iexact=deck_language_name)
    except ObjectDoesNotExist:
        return render(request, 'cards/deck_not_learning_detail.html', context)

    if request.method == 'POST':
        request, deckmembership = card_membership_update(request, request.POST.get('card_id'), request.POST.get('status'))
        return redirect(request.META.get('HTTP_REFERER'))

    if request.method == 'GET':
        try:
            card = deck.browse_new()
        except ObjectDoesNotExist:
            message.warning(request, 'You have gone through all the cards in this deck.')
            return render(request, 'cards/deck_detail.html', context)

    context = {
        'deck': deck,
        'card': card,
        'membership': deckmembership or {},
        'card_language_matches_a_deck': True,
    }

    return render(request, 'cards/browse_deck.html', context)

def language_detail(request, language_name):
    language = get_object_or_404(Language, name=language_name)
    deck = {}

    if request.user.is_authenticated:
        try:
            deck = Deck.objects.get(person=request.user.person, language=language)
        except ObjectDoesNotExist:
            pass

    context = {
        'language': language,
        'deck': deck,
    }
    return render(request, 'cards/language_detail.html', context)

@login_required
def app_home(request):
    return render(request, 'cards/home.html', {})

def public_splash_page(request):
    return render(request, 'cards/splash.html', {})

def home(request):
    if request.method == 'POST':
        return login_page(request)

    if request.user.is_authenticated:
        return app_home(request)

    return public_splash_page(request)

@login_required
def deck_detail(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id, person=request.user.person)
    context = {
        'deck': deck,
    }
    return render(request, 'cards/deck_detail.html', context)


@login_required
def translation_add(request, card_id):
    if request.method == 'POST':
        language_name = request.POST.get('language_name')
        language = get_object_or_404(Language, name=language_name)
        card = get_object_or_404(Card, pk=card_id)
        # TODO: validate that text is set
        cardtranslation_text = request.POST.get('text')
        literal_translation = request.POST.get('literal') or ''

        cardtranslation = CardTranslation(
            card=card,
            language=language,
            text=cardtranslation_text,
            literal=literal_translation
        )
        cardtranslation.save()
        messages.success(request, 'Added your new card translation')

    return redirect('card_detail', card_id)

@login_required
def relations_add(request, card_id):
    related = request.POST.getlist('related_cards') if request.method == 'POST' else None
    if related == None:
        messages.error(request, 'No related phrase selected')
    else:
        card = get_object_or_404(Card, pk=card_id)
        starting_relations = card.see_also.all().count()
        bad_relations = 0
        for related_card_id in related:
            try:
                new_related_card = Card.objects.get(pk=related_card_id)
                card.see_also.add(new_related_card)
            except ObjectDoesNotExist:
                bad_relations += 1
        new_relations = card.see_also.all().count() - starting_relations or 0
        if new_relations:
            messages.success(request, "Added new %d related phrases" % new_relations)
        if bad_relations:
            messages.warning(request, "Errors adding %d new relations" % bad_relations)
    return redirect('card_detail', card_id)

@login_required
def deck_add(request):
    if request.method == 'POST':
        language_name = request.POST.get('language_name')
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

    context = {}

    if request.method == 'GET':
        return render(request, 'cards/deck_add.html', context)

@login_required
def card_add(request):
    if request.method == 'POST':
        card_language = Language.objects.get(
            name__iexact=request.POST.get('card_language_name'))
        cardtranslation_language = Language.objects.get(
            name__iexact=request.POST.get('cardtranslation_language_name'))
        deck = Deck.objects.get(language=card_language, person=request.user.person)

        card = Card.objects.create(language=card_language, text=request.POST.get('card_text'))
        cardtranslation = CardTranslation.objects.create(
            language=cardtranslation_language,
            text=request.POST.get('cardtranslation_text'),
            card=card
        )
        deckmembership = DeckMembership.objects.create(
            card=card,
            deck=deck,
            status='learning'
        )

        messages.success(request, 'Successfully created your new card!')
        return redirect('card_detail', card.id)

    context = {}
    return render(request, 'cards/card_add.html', context)

@login_required
def user_profile(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'person update':
            person = request.user.person
            set_languages = request.POST.getlist('speaks_languages')
            person.speaks_languages.set(Language.objects.filter(name__in=set_languages))
            person.name = request.POST.get('name')
            request.user.email = request.POST.get('email')
            person.save()
            request.user.save()
            messages.success(request, 'Account information updated')
        if request.POST.get('action') == 'password change':
            if request.user.check_password(request.POST.get('password')) == False:
                messages.error(request, 'Invalid password')
            elif request.POST.get('new_password') != request.POST.get('repeat_password'):
                messages.error(request, 'Your passwords did not match')
            else:
                request.user.set_password(request.POST.get('new_password'))
                request.user.save()
                messages.success(request, 'I think we\'ve updated your password')

    return render(request, 'cards/user_profile.html', {})

@login_required
def my_deck(request, deck_language_name):
    context = {}
    try:
        context.update({
            'deck': Deck.objects.get(person=request.user.person, language__name__iexact=deck_language_name)
        })
    except ObjectDoesNotExist:
        return render(request, 'cards/deck_not_learning_detail.html', context)

    return render(request, 'cards/deck_detail.html', context)

@login_required
def index(request):
    context = {
        'cards': Card.objects.all(),
    }
    return render(request, 'cards/index.html', context)
