from django.urls import path
from . import views

app_name = 'userManageSys'


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('find/',views.find, name='find'),
    path('user_homepage/',views.user_homepage, name='user_homepage'),
    path('service_homepage/',views.service_homepage, name='service_homepage'),
    path('manager_homepage/',views.manager_homepage, name='manager_homepage'),
    path('goods_detail/',views.goods_detail, name='goods_detail'),
    path('chat_room/', views.chat_room, name='chat_room'),
    path('add_goods/', views.add_goods, name='add_goods'),
    path('del_goods/', views.del_goods, name='del_goods'),
    path('edit_goods/', views.edit_goods, name='edit_goods'),
    path('add_service/', views.add_service, name='add_service'),
    path('del_service/', views.del_service, name='del_service'),
    path('edit_service/', views.edit_service, name='edit_service'),
    path('online_data_center/', views.online_data_center, name='online_data_center'),
    path('history_data_center/', views.history_data_center, name='history_data_center'),
    path('test/', views.test, name='test'),
]