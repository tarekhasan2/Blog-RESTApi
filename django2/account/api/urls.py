
from django.contrib import admin
from django.urls import path


from account.api import views
app_name = "account"

urlpatterns = [


	path('account/api/register/', views.UserCreateAPIView.as_view(), name= 'register'),
	path('account/api/login/', views.UserLoginAPIView.as_view(), name= 'login'),


]
