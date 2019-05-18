

from django.contrib import admin
from django.urls import path


from . import views
app_name = "account"

urlpatterns = [

	path('account/', views.login_view, name= 'login'),
	path('account/register', views.register_view, name= 'register'),
	path('account/logout', views.logout_view, name= 'logout'),
	#path('comments/<int:id>/delete', views.comment_delete, name = 'delete'),


]










