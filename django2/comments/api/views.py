from django.contrib.contenttypes.models import ContentType
from rest_framework.generics import (
	RetrieveAPIView,
	ListAPIView,
	DestroyAPIView,
	UpdateAPIView,
	CreateAPIView,
	RetrieveUpdateAPIView
	)  

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from django.db.models import Q
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
	)
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination

from comments.api.serializers import (
	CommentListSerializer,
	CommentDetailSerializer,
	create_comment_serializer,
	CommentEditSerializer
	)



from comments.models import Comment

from rest_framework.filters import (
		SearchFilter,
		OrderingFilter,
	)
from posts.models import Post 

from posts.api.permissions import IsOwnerOrReadOnly




class CommentEditAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
	queryset = Comment.objects.filter(id__gte=0)
	serializer_class = CommentEditSerializer

	def put(self, request, *args,  **kwargs):
		return self.update(request, *args, **kwargs)



	def delete(self, request, *args,  **kwargs):
		return self.destroy(request, *args, **kwargs)
	



class CommentCreateAPIView(CreateAPIView):
	queryset = Comment.objects.all()
	#serializer_class = PostCreateUpdateSerializer
	permission_classes = [IsAuthenticated] 
	def get_serializer_class (self):
		model_type = self.request.GET.get("type")
		id = self.request.GET.get('id')
		parent_id = self.request.GET.get("parent_id", None)
		return create_comment_serializer(
			model_type=model_type,
			id=id, 
			parent_id=parent_id,
			user = self.request.user,
			)



class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
	queryset = Comment.objects.filter(id__gte=0)
	serializer_class = CommentDetailSerializer
	#lookup_field = "id"
	def put(self, request, *args,  **kwargs):
		return self.update(request, *args, **kwargs)


	def delete(self, request, *args,  **kwargs):
		return self.destroy(request, *args, **kwargs)
	



class CommentListAPIView(ListAPIView):

	#queryset = Comment.objects.all()
	serializer_class = CommentListSerializer
	pagination_class = PostPageNumberPagination
	filter_backends = [SearchFilter]
	
	search_fields = ['content','user__first_name']
	
	def get_queryset(self, *args, **kwargs):
		#queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)

		queryset_list = Comment.objects.all()
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query)|
				Q(user__last_name__icontains=query)
				).distinct()
		return queryset_list


