from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from markdown_deux import markdown
from comments.models import Comment
from .utils import get_read_time
from django.contrib.contenttypes.models import ContentType

# Create your models here.
# MVC
##
#Some defult ModelManager is:
#Post.objects.all()
#Post.objects.create()

class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		#Post.objects.all()= super(PostManager, self).all()
		return super(PostManager, self).filter(draf=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete = True)
	title = models.CharField(max_length=120)
	slug = models.SlugField(unique= True)
	image = models.ImageField(null=True, blank= True,
		upload_to=upload_location, 
		width_field= "width_field",
		height_field="height_field")
	draf = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add= False)
	read_time = models.IntegerField(default=0)
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	content = models.TextField()
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


	objects = PostManager()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("posts:read" , kwargs={"id":self.id})
		#return ("posts:read",(),{"slug":self.slug})
		#return "/posts/%s/" %(self.id)

	def get_api_url(self):
		return reverse("posts-api:details" , kwargs={"id":self.id})
	
	def get_markdown(self):
		content = self.content
		markdown_text = markdown(content)
		return mark_safe(markdown_text)

		

	class Meta:
		ordering = ["-timestamp", "-updated"]

	@property
	def comments(self):
		item = self
		qs = Comment.objects.filter_by_instance(item)
		return qs

	@property
	def get_content_type(self):
		item = self
		content_type = ContentType.objects.get_for_model(item.__class__)
		return content_type



def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug= slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)

	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)
	if instance.content:
		html_string = instance.get_markdown()
		read_time = get_read_time(html_string)
		instance.read_time = read_time
pre_save.connect(pre_save_post_receiver, sender=Post)
			