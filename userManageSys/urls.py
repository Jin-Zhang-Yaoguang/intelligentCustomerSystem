from django.urls import path
from . import views

app_name = 'userManageSys'


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('find/',views.find, name='find')
]