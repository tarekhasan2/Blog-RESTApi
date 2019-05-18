
from django.contrib import admin
from django.urls import path


from comments.api import views
app_name = "comments"

urlpatterns = [

	path('comments/api/', views.CommentListAPIView.as_view(), name= 'list'),
	path('comments/api/create/', views.CommentCreateAPIView.as_view(), name= 'create'),
	path('comments/api/<int:pk>/details', views.CommentDetailAPIView.as_view(), name= 'details'),
	path('comments/api/<int:pk>/edit', views.CommentEditAPIView.as_view(), name= 'edit'),

	#path('comments/api/<int:id>/delete', views.comment_delete, name = 'delete'),


]
