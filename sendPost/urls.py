from django.urls import path
from . import views

app_name = 'sendPost'
urlpatterns = [
    path('', views.indexView, name='index'),
    path('reView/', views.reView, name='reView'),
    path('results/', views.results, name='results'),
    path('errorResult/<int:result_file_num>/', views.errorResult, name='errorResult'),
    path('create/', views.create_account, name='create_account'),
    path('login/', views.account_login, name='login'),
    path('download/<str:result_file_num>/', views.download, name='download')
]