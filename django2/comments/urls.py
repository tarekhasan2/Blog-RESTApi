


from django.contrib import admin
from django.urls import path


from . import views
app_name = "comments"

urlpatterns = [

	path('comments/<int:id>/', views.comment_tread, name= 'tread'),

	path('comments/<int:id>/delete', views.comment_delete, name = 'delete'),




]
