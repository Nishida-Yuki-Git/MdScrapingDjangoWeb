from django.urls import path
from . import views

app_name = 'sendPost'
urlpatterns = [
    path('', views.IndexView, name='index'),
    path('create/', views.create_account, name='create_account'),
    path('login/', views.account_login, name='login'),
]