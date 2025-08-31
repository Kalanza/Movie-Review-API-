from rest_framework import viewsets, permissions, filters
from django.contrib.auth.models import User
from .models import Review
from .serializers import UserSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class UserViewSet(viewsets.ModelViewSet):
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
