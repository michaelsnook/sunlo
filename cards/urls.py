from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^deck/(?P<deck_id>[0-9]+)/$', views.deck_detail, name='deck_detail'),
    url(r'^card/(?P<card_id>[0-9]+)/$', views.card_detail, name='card_detail'),
    url(r'^language/(?P<language_id>[0-9]+)/$', views.language_detail, name='language_detail'),
    #url(r'^cards/(?P<card_language>[0-9]+)/$', views.card_language, name='card_language'),
]
