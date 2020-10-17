from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('login', views.login),
    path('log_off', views.log_off),
    path('quotes',views.qoutes),
    path('add_quote',views.add_quote),
    path('user/<int:user_id>',views.user_quotes),
    path('myaccount/<int:user_id>',views.edit_account),
    path('add_to_liked/<int:quote_id>',views.add_to_liked),
    path('delete/<int:quote_id>',views.delete_quote),
    path('update_account',views.change_account)
]