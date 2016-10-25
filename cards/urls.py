from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^$', views.home, name='home'),
    url(r'^me/$', views.user_profile, name='user_profile'),
    url(r'^login/$', views.login_page, name='login_page'),
    url(r'^signup/$', views.user_register, name='user_register'),
    url(r'^logout/$', views.logout_page, name='logout_page'),
    url(r'^deck/add/$', views.deck_add, name='deck_add'),
    url(r'^card/add/$', views.card_add, name='card_add'),
    url(r'^deck/(?P<deck_language_name>[a-zA-Z_-]+)/$', views.my_deck, name='my_deck'),
    url(r'^deck/(?P<deck_id>[0-9]+)/$', views.deck_detail, name='deck_detail'),
    url(r'^card/(?P<card_id>[0-9]+)/$', views.card_detail, name='card_detail'),
    url(r'^card/(?P<card_id>[0-9]+)/update/$', views.membership_update, name='membership_update'),
    url(r'^language/(?P<language_id>[0-9]+)/$', views.language_detail, name='language_detail'),
    #url(r'^cards/(?P<card_language>[0-9]+)/$', views.card_language, name='card_language'),
]
