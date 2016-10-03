from django.contrib import admin
from .models import Card, CardTranslation, Person, Language, Deck


admin.site.register(Card)
admin.site.register(CardTranslation)
admin.site.register(Person)
admin.site.register(Language)
admin.site.register(Deck)
