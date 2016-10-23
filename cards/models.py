from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import capfirst


class Language(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Card(models.Model):
    # nuggets of the languages people are trying to learn
    text = models.TextField()
    language = models.ForeignKey(Language)
    see_also = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.language.name + ' - ' + self.text


class CardTranslation(models.Model):
    # translations of target cards into other languages people already know
    text = models.TextField()
    literal = models.TextField(blank=True)
    card = models.ForeignKey(Card)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return self.language.name + ' learning ' + self.card.language.name + ': ' + self.card.text


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    facebook_name = models.CharField(max_length=200, blank=True)

    speaks_languages = models.ManyToManyField(Language, related_name='speakers')

    def salutation(self):
        return self.user.first_name or self.user.username

    def username(self):
        return self.user.username

    def name(self):
        return self.user.first_name + ' ' + self.user.last_name if self.user.first_name else self.username()

    def email(self):
        return self.user.email

    def __str__(self):
        return self.name() or self.username()


class Deck(models.Model):
    # one person owns one or more decks
    person = models.ForeignKey(Person)
    language = models.ForeignKey(Language)
    cards = models.ManyToManyField(Card, through='DeckMembership')

    def learning_cards(self):
        return Card.objects.filter(deck=self, deckmembership__status="learning")

    def learned_cards(self):
        return Card.objects.filter(deck=self, deckmembership__status="learned")

    def rejected_cards(self):
        return Card.objects.filter(deck=self, deckmembership__status="rejected")

    def suggestions(self):
        return Card.objects.filter(deck=self, deckmembership__status="pending")

    #def unseen(self):
    #    return Card.objects.filter(deckmembership__status="unseen")

    def memberships(self):
        return DeckMembership.objects.filter(deck=self)

    def language_name(self):
        return self.language.name

    def translation_languages(self):
        return self.person.knows

    def __str__(self):
        return capfirst(self.person.name()) + ', ' + self.language.code

class DeckMembership(models.Model):
    deck = models.ForeignKey(Deck)
    card = models.ForeignKey(Card)
    status = models.SlugField()

    def __str__(self):
        return self.deck.person.name() + self.card.text

class Suggestion(models.Model):
    suggested_by = models.ForeignKey(Person, on_delete=models.CASCADE)
    suggestion_comment = models.TextField()
    def __str__(self):
        return self.suggested_by.name + ' suggests a ' + self.deck.language.name + ' for ' + self.deck.person.name
