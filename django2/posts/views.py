from django.contrib import messages

from urllib.parse import quote_plus

from django.utils import timezone
from django.db.models import Q
from comments.models import Comment
from comments.form import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .form import PostForm
from .models import Post
from .utils import get_read_time 

from django.core.paginator import Paginator
from django.shortcuts import render
# Create your views here.

def posts_home(request):
	today = timezone.now().date()
	query_list = Post.objects.active()## it shows active ModelManager that created in models.py
	#query_list = Post.objects.filter(draf=False).filter(publish__lte=timezone.now())
	if request.user.is_staff or request.user.is_superuser:
		query_list = Post.objects.all()
	##for search option
	query = request.GET.get("q")
	if query:
		query_list = query_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()
	###
	###for pagination
	paginator = Paginator(query_list, 4) # Show 25 contacts per page

	page = request.GET.get('page')
	########
	queryset = paginator.get_page(page)
	context = {
		"title" :"List",
		"objects_list" : queryset,
		"today" : today,

	}
	
	return render (request, 'post_home.html', context)


def create(request):
	if request.user.is_staff or request.user.is_superuser:
		
		form = PostForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			messages.success(request, "Successfully Created")
			return HttpResponseRedirect(instance.get_absolute_url())
		context = {
			"form":form
		}
		return render(request, 'create.html', context)
	else:
		raise Http404


def read(request, id= None):
	item = get_object_or_404(Post, id = id)
	if item.publish > timezone.now().date() or item.draf :
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(item.content)

	#print(get_read_time(item.get_markdown()))
	## next two field used without modelManager
	#content_type = ContentType.objects.get_for_model(Post)
	#obj_id = item.id
	initial_data = {
		"content_type": item.get_content_type,
		"object_id": item.id
	}
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get("object_id")
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try :
			parent_id = int(request.POST.get("parent_id"))
		except :
			parent_id = None
		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists():
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
				user = request.user,
				content_type =content_type,
				object_id = obj_id,
				content = content_data,
				parent = parent_obj,
			)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())




	#comments = Comment.objects.filter_by_instance(item)
	comments = item.comments
	context = {
	
	"item" : item,
	"share_string" : share_string,
	"comments" :comments,
	"comment_form" : form ,
	
	
	}
	return render(request, 'read.html', context)


def update(request, id=None):
	if request.user.is_staff or request.user.is_superuser:
		
		instance = get_object_or_404(Post, id = id)
		form = PostForm(request.POST or None,request.FILES or None ,instance= instance)
		if form.is_valid():
			instance = form.save(commit=False) 
			instance.save()
			messages.success(request, "<a href='#'>Successfully</a> Updated", extra_tags ="html_teg")
			return HttpResponseRedirect(instance.get_absolute_url())
		context = {
		
			"item": instance,
			"title": instance.title,
			"form" : form
		
		}
		return render(request, 'create.html', context)
	else:
		raise Http404


def delete(request, id=None):
	if request.user.is_staff or request.user.is_superuser:
		
		instance = get_object_or_404(Post, id = id)
		instance.delete()
		return redirect ('posts:list')
	else:
		raise Http404
