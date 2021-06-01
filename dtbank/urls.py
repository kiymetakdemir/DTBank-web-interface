from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('createtables', views.createtables, name='createtables'),
    path('login/', views.userloginpage, name='login'),
    path('managerlogin/', views.managerlogin, name='managerlogin'),
    path('userdirect/', views.login, name="userdirect"),
    path('managerloginpage/', views.managerloginpage, name='managerloginpage'),
    path('managerdirect/', views.managerlogin, name="managerdirect"),
    path('managerhome/', views.managerhome, name="managerhome"),
    path('userhome/', views.userhome, name="userhome"),
    path('saveuser/', views.saveuser, name='saveuser'),
    path('adduser/', views.adduser, name = 'adduser'),
    path('encrypt/', views.encrypt_passwords, name='encrypt')


]
