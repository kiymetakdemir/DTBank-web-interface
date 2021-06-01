from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.userloginpage, name='login'),
    path('managerlogin/', views.managerlogin, name='managerlogin'),
    path('userdirect/', views.login, name="userdirect"),
    path('managerloginpage/', views.managerloginpage, name='managerloginpage'),
    path('managerdirect/', views.managerlogin, name="managerdirect"),
    path('managerhome/', views.managerhome, name="managerhome"),
    path('userhome/', views.userhome, name="userhome"),
    path('saveuser/', views.saveuser, name='saveuser'),
    path('encrypt/', views.encrypt_passwords, name='encrypt'),
    path('update_affinity/', views.update_affinity),
    path('delete_drug/', views.delete_drug),
    path('delete_protein/', views.delete_protein),
    path('viewtable/<str:tablename>', views.viewtable),
    path('viewusers/', views.viewusers),
    path('updatecontributors/', views.updateContributors)


]
