from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name="user_login"),
    path('success/', views.success, name="user_success"),
    path('logout/', views.user_logout, name="user_logout"),
    path('account_details/', views.account_details, name="account_details"),
    path('register_view/', views.register_view, name= "register_view"),
    path('deposit/', views.deposit, name= "deposit"),
    path('withdrawl/',views.withdrawl, name= 'withdrawl'),

]