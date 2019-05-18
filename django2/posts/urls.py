


from django.contrib import admin
from django.urls import path
from . import views
app_name = "posts"

urlpatterns = [
    
    path('', views.posts_home, name = 'list'),
    path('posts/create', views.create, name = 'create'),
    path('posts/<int:id>/', views.read, name= 'read'),
    #path('posts/<slug:slug>/', views.read, name= 'read'),
    path('posts/<int:id>/update', views.update, name='update'),
    path('posts/<int:id>/delete', views.delete, name = 'delete')


]
