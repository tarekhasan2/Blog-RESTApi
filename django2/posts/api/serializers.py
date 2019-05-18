from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
	)


from comments.api.serializers import CommentListSerializer
from comments.models import Comment


from posts.models import Post 


detail_url = HyperlinkedIdentityField(
		view_name = 'posts-api:details',
		#lookup_field = 'id' 
		)

delete_url = HyperlinkedIdentityField(
		view_name = 'posts-api:delete',
		#lookup_field = 'id' 
		)


class PostListSerializer(ModelSerializer):
	user = SerializerMethodField()
	url = detail_url
	class Meta:
		model = Post
		fields = [
			'url',
			'user',
			'title',
			'slug',
			'content',
			'id',
		]

	def get_user(self, obj):
		return str(obj.user.username)

class PostDetailSerializer(ModelSerializer):
	user = SerializerMethodField()
	image = SerializerMethodField()
	html = SerializerMethodField()
	comments = SerializerMethodField()
	delete = delete_url
	class Meta:
		model = Post
		fields = [
			'delete',
			'user',
			'title',
			'slug',
			'content',
			'html',
			'image',
			'comments',
		]
	def get_user(self, obj):
		return str(obj.user.username)

	def get_image(self, obj):
		try:
			image = obj.image.url
		except:
			image = None

		return image
	def get_html (self, obj):
		return obj.get_markdown()

	def get_comments(self, obj):
		#content_type = obj.get_content_type
		#ovject_id = obj.id
		c_qs = Comment.objects.filter_by_instance(obj)
		comments = CommentListSerializer(c_qs, many=True).data
		return comments


class PostCreateUpdateSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
			'title',
			'content',
			'publish',
			
		]