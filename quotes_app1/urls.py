from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('quotes', views.quotes),
    path('add_quote', views.add_quote),
    path('quotes/<int:quote_id>/add_favorite', views.add_favorite),
    path('quotes/<int:quote_id>/remove_favorite', views.remove_favorite),
    path('quotes/<int:quote_id>/edit_quote', views.edit_quote),
    path('quotes/<int:quote_id>/update_quote', views.update_quote),
    path('quotes/<int:quote_id>/delete_quote', views.delete_quote),
    path('<int:profile_id>/user_profile', views.user_profile),
]