from django.urls import path

from . import views

urlpatterns = [
    path('admin_login', views.admin_login, name='admin_login'),
    path('att_login', views.att_login, name='att_login'),
    path('register', views.register, name='register'),
    path('create', views.create, name='create'),
    path('addusers', views.addusers, name='addusers'),
    path('update_meeting', views.update_meeting, name='update_meeting'),
    path('update_user', views.update_user, name='update_user'),
    path('update_user_meeting', views.update_user_meeting, name='update_user_meeting'),
    path('create_meeting_list', views.create_meeting_list, name='create_meeting_list'),
    path('att_meeting_list', views.att_meeting_list, name='att_meeting_list'),
    path('delete_users_meeting', views.delete_users_meeting, name='delete_users_meeting'),
    path('delete_meeting', views.delete_meeting, name='delete_meeting'),
]