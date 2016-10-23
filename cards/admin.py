from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Card, CardTranslation, Person, Language, Deck, DeckMembership


admin.site.register(Deck)
admin.site.register(DeckMembership)
admin.site.register(Language)

class CardTranslationInline(admin.TabularInline):
    model = CardTranslation

class CardAdmin(admin.ModelAdmin):
    model= Card
    inlines = (CardTranslationInline, )

admin.site.register(Card, CardAdmin)

class DeckInline(admin.TabularInline):
    model = Deck

class PersonAdmin(admin.ModelAdmin):
    model = Person
    can_delete = False
    verbose_name_plural = 'people'
    inlines = (DeckInline, )

admin.site.register(Person, PersonAdmin)
