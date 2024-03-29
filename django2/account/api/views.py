from rest_framework.generics import (
	RetrieveAPIView,
	ListAPIView,
	DestroyAPIView,
	UpdateAPIView,
	CreateAPIView,
	RetrieveUpdateAPIView
	)  
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView


from django.db.models import Q
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
	)
from .serializers import (
	UserCreateSerializer,
	UserLoginSerializer
	)

from rest_framework.filters import (
		SearchFilter,
		OrderingFilter,
	)

from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateAPIView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserCreateSerializer
	
	
	
class UserLoginAPIView(APIView):
	permissions_classes = [AllowAny]
	serializer_class = UserLoginSerializer

	def post (self, request, *args, **kwargs):
		data = request.data
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data = serializer.data
			return Response(new_data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


		











