from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
	path('register', views.UserRegister.as_view(), name='register'),
	path('login', views.LoginView.as_view(), name='login'),
	path('user', views.UserView.as_view(), name='user'),
	path('user-token', views.get_usertoken, name='user-token'),
	path('logout', views.UserLogout.as_view(), name='logout'),
	path('get-userprofile', views.get_userprofile, name='profile'),
	path('get-publicprofile', views.GerPublicProfile.as_view(), name='publicprofile'),
	path('update-userprofile', views.update_userprofile, name='update-userprofile'),
]