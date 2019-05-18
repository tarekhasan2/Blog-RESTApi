
from django.contrib import admin
from django.urls import path
from posts.api import views
app_name = "posts"

urlpatterns = [
	path('api/posts/', views.PostListAPIView.as_view(), name = 'list'),
	path('api/posts/create', views.PostCreateAPIView.as_view(), name = 'create'),
    #path('posts/create', views.create),
    path('api/posts/<int:pk>', views.PostDetailAPIView.as_view(), name= 'details'),
    path('api/posts/<int:pk>/update', views.PostUpdateAPIView.as_view(), name= 'update'),
    path('api/posts/<int:pk>/delete', views.PostDeleteAPIView.as_view(), name= 'delete'),
  
]
