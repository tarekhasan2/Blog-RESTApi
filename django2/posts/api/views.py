from rest_framework.generics import (
	RetrieveAPIView,
	ListAPIView,
	DestroyAPIView,
	UpdateAPIView,
	CreateAPIView,
	RetrieveUpdateAPIView
	)  
from django.db.models import Q
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
	)
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination

from .serializers import PostDetailSerializer, PostListSerializer, PostCreateUpdateSerializer
from posts.models import Post
from rest_framework.filters import (
		SearchFilter,
		OrderingFilter,
	)
from .permissions import IsOwnerOrReadOnly



class PostListAPIView(ListAPIView):
	serializer_class = PostListSerializer
	pagination_class = PostPageNumberPagination
	filter_backends = [SearchFilter]
	search_fields = ['title','content','user__first_name']

	def get_queryset(self, *args, **kwargs):
		#queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
		queryset_list = Post.objects.all()
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query)|
				Q(user__last_name__icontains=query)
				).distinct()
		return queryset_list


class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	#lookup_field = 'id'


class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	permission_classes = [IsAuthenticated] 

	def perform_create(self, serializer):
		serializer.save(user = self.request.user)



class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

	#lookup_field = 'slug'


	def perform_update(self, serializer):
		serializer.save(user = self.request.user)





class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	#lookup_field = 'slug'


