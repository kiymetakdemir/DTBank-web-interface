from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='dtbank-home'),
    path('login/', views.login, name='dtbank-login'),
    path('managerlogin/', views.managerlogin, name='managerlogin'),
    path('userdirect/', views.login, name="userdirect"),
    path('managerloginpage/', views.managerloginpage, name='managerloginpage'),
    path('managerdirect/', views.managerlogin, name="managerdirect"),
    path('managerhome/', views.managerhome, name="managerhome"),
    path('userhome/', views.userhome, name="userhome")
    #path('createtables/', views.my_custom_sql, name = "createtables")
    #path('adduser/', views.adduser, name='dtbank-adduser')
    #path('userlogin/', views.userlogin, name='dtbank-userlogin'),
    #path('managerlogin/', views.managerlogin, name='dtbank-managerlogin')

]
