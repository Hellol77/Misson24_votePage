# users/urls.py

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('main/', views.main_view, name='main'),
    path('', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.PostUpload, name='register'),
    path('assess/', views.peerGroup_view, name='assess'),
    path('assess/<int:pk>/', views.assessDetail_view, name='assess_detail'),

]