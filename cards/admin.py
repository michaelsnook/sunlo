from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Card, CardTranslation, Person, Language, Deck



admin.site.register(Language)
admin.site.register(Deck)

class CardTranslationInline(admin.TabularInline):
    model = CardTranslation

class CardAdmin(admin.ModelAdmin):
    inlines = (CardTranslationInline, )

admin.site.register(Card, CardAdmin)

class PersonInline(admin.StackedInline):
    model = Person
    can_delete = False
    verbose_name_plural = 'people'

class UserAdmin(BaseUserAdmin):
    inlines = (PersonInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
