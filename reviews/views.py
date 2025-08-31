from rest_framework import viewsets, permissions, filters, generics
from django.contrib.auth.models import User
from .models import Review
from .serializers import UserSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [permissions.AllowAny]

# Registration endpoint
class RegisterView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [permissions.AllowAny]

class ReviewViewSet(viewsets.ModelViewSet):
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	search_fields = ['movie_title', 'rating']
	ordering_fields = ['rating', 'created_date']
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get_queryset(self):
		queryset = Review.objects.all()
		movie_title = self.request.query_params.get('movie_title')
		ratings = self.request.query_params.getlist('rating')
		if movie_title:
			queryset = queryset.filter(movie_title__iexact=movie_title)
		if ratings:
			queryset = queryset.filter(rating__in=ratings)
		return queryset

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		if instance.user != request.user:
			return Response({'detail': 'You do not have permission to edit this review.'}, status=status.HTTP_403_FORBIDDEN)
		return super().update(request, *args, **kwargs)

	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		if instance.user != request.user:
			return Response({'detail': 'You do not have permission to delete this review.'}, status=status.HTTP_403_FORBIDDEN)
		return super().destroy(request, *args, **kwargs)

	@action(detail=False, methods=['get'], url_path='movie/(?P<title>[^/.]+)')
	def reviews_by_movie(self, request, title=None):
		queryset = self.get_queryset().filter(movie_title__iexact=title)
		paginator = PageNumberPagination()
		paginator.page_size = 10
		page = paginator.paginate_queryset(queryset, request)
		serializer = self.get_serializer(page, many=True)
		return paginator.get_paginated_response(serializer.data)
