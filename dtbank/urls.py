from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dtbank-home'),
    path('login/', views.login, name='dtbank-login')
]
