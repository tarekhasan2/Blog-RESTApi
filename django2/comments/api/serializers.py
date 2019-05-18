from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model


from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField,
	ValidationError
	)


from comments.models import Comment 
from posts.models import Post


User = get_user_model()
def create_comment_serializer(model_type='post', id=None, parent_id=None, user=None):
	class CommentCreateSerializer(ModelSerializer):
		class Meta:
			model = Comment
			fields = [
				'id',
				'content',
				'parent',
				'timestamp',
			]
		def __init__(self, *args, **kwargs):
			self.model_type = model_type
			self.id = id
			self.parent_obj = None
			if parent_id:
				parent_qs = Comment.objects.filter(id=parent_id)
				if parent_qs.exists() and parent_qs.count() ==1:
					self.parent_obj = parent_qs.first()

			return super(CommentCreateSerializer, self).__init__(*args, **kwargs)


		def validate(self, data):
			model_type = self.model_type
			model_qs = ContentType.objects.filter(model=model_type)
			if not model_qs.exists() or model_qs.count() != 1:
				raise ValidationError("This is not a valid content type")
			SomeModel = model_qs.first().model_class()
			obj_qs = SomeModel.objects.filter(id = self.id)
			if not obj_qs.exists() or obj_qs.count() != 1:
				raise ValidationError("This is not a id for this content type")
			return data

		def create(self, validate_data):
			content = validate_data.get("content")
			if user:
				main_user = user
			else:
				main_user = User.objects.all().first()
			model_type = self.model_type
			id = self.id
			parent_obj = self.parent_obj
			comment = Comment.objects.create_by_model_type(
				model_type,
				id,
				content,
				main_user,
				parent_obj = parent_obj,
				)
			return comment
	return CommentCreateSerializer		





detail_url = HyperlinkedIdentityField(
		view_name = 'comments-api:details',
		#lookup_field = 'id' 
		)

class CommentListSerializer(ModelSerializer):
	reply_count = SerializerMethodField()
	details = detail_url
	class Meta:
		model = Comment
		fields = [
			'id',
			'object_id',
			'parent',
			'timestamp',
			'reply_count',
			'details',
		]
	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0


class CommentDetailSerializer(ModelSerializer):
	replies = SerializerMethodField() 
	reply_count = SerializerMethodField()
	#content_obj_url = SerializerMethodField()
	class Meta:
		model = Comment
		fields = [
			'id',
			'content_type',
			'object_id',
			'content',
			'timestamp',
			'reply_count',
			#'content_obj_url',
			'replies',
			
		]
		read_only_fields = [
			'content_type',
			'object_id',
			'replies',
			'reply_count'

		]

	def get_replies(self, obj):
		if obj.is_parent:
			return CommentChildSerializer(obj.children(), many=True ).data
		return None

	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0

	#def get_content_obj_url(self, obj):
	#	return obj.content_object.get_api_url()
	

class CommentChildSerializer(ModelSerializer):

	class Meta:
		model = Comment
		fields = [
			'id',
			'content',
			'timestamp',
		]
	



class CommentEditSerializer(ModelSerializer):
	 
	class Meta:
		model = Comment
		fields = [
			'id',
			'content_type',
			'object_id',
			'content',
			'timestamp',
	
		]

	


		