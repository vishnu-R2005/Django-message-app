from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),     # 👈 default route shows login page
    path('home/', views.index, name='index'),     # 👈 protected home page
    path('messages/', views.message_list, name='message_list'),
    path('register/', views.register_view, name='register'), 
    path('logout/', views.logout_view, name='logout'),
]
