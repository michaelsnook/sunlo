from __future__ import unicode_literals

from django.db import models


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
    # tie this into session middleware...
    name = models.CharField(max_length=200)
    facebook_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    languages = models.ManyToManyField(Language)

    # learning = models.ManyToManyField(Language)
    # understands = models.ManyToManyField(Language)
    # teaches = models.ManyToManyField(Language)

    def __str__(self):
        return self.name


class Deck(models.Model):
    # one person owns one or more decks
    person = models.ForeignKey(Person)
    language = models.ForeignKey(Language, blank=True)
    cards = models.ManyToManyField(Card, blank=True)

    #def languages(self):
    #    return self.person.languages

    def __str__(self):
        return self.person.name

"""
class SuggestionStatus(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Suggestion(models.Model):
    card = models.ForeignKey(Card)
    deck = models.ForeignKey(Deck)
    status = models.ForeignKey(SuggestionStatus)
    suggested_by = models.ForeignKey(Person)
    def __str__(self):
        return self.suggested_by.name + ' suggests a ' + self.deck.language.name + ' for ' + self.deck.person.name
"""
