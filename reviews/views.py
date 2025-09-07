from .omdb_utils import fetch_movie_info
from rest_framework import viewsets, permissions, filters, generics
from django.contrib.auth.models import User
from .models import Review, UserProfile, ReviewLike, ReviewComment
from .serializers import UserSerializer, ReviewSerializer, UserProfileSerializer, ReviewLikeSerializer, ReviewCommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        user = self.get_object()
        profile, created = UserProfile.objects.get_or_create(user=user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        user = self.get_object()
        reviews = user.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
class UserProfileViewSet(viewsets.ModelViewSet):
	queryset = UserProfile.objects.all()
	serializer_class = UserProfileSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return UserProfile.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class ReviewLikeViewSet(viewsets.ModelViewSet):
	queryset = ReviewLike.objects.all()
	serializer_class = ReviewLikeSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return ReviewLike.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class ReviewCommentViewSet(viewsets.ModelViewSet):
	queryset = ReviewComment.objects.all()
	serializer_class = ReviewCommentSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

# Registration endpoint
class RegisterView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [permissions.AllowAny]

class ReviewViewSet(viewsets.ModelViewSet):
	@action(detail=False, methods=['get'], url_path='recommendations')
	def recommendations(self, request):
		if not request.user.is_authenticated:
			return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
		# Step 1: Get movies the user rated 4 or 5
		user_high_rated = Review.objects.filter(user=request.user, rating__gte=4)
		high_rated_titles = user_high_rated.values_list('movie_title', flat=True)
		# Step 2: Find other users who also rated these movies highly
		similar_reviews = Review.objects.filter(movie_title__in=high_rated_titles, rating__gte=4).exclude(user=request.user)
		similar_users = similar_reviews.values_list('user', flat=True).distinct()
		# Step 3: Find other movies these users rated highly, excluding movies the current user has already reviewed
		recommended_reviews = Review.objects.filter(user__in=similar_users, rating__gte=4).exclude(movie_title__in=high_rated_titles)
		recommended_titles = recommended_reviews.values_list('movie_title', flat=True).distinct()
		# Step 4: Return a list of recommended movie titles
		return Response({'recommended_movies': list(recommended_titles)})
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
		# Fetch OMDB info for the movie
		movie_info = fetch_movie_info(title)
		return paginator.get_paginated_response({
			'movie_info': movie_info,
			'reviews': serializer.data
		})

	def retrieve(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.get_serializer(instance)
		movie_info = fetch_movie_info(instance.movie_title)
		data = serializer.data
		data['movie_info'] = movie_info
		return Response(data)

	@action(detail=False, methods=['get'], url_path='most-liked/(?P<title>[^/.]+)')
	def most_liked_reviews(self, request, title=None):
		queryset = self.get_queryset().filter(movie_title__iexact=title)
		queryset = sorted(queryset, key=lambda r: r.likes.count(), reverse=True)
		paginator = PageNumberPagination()
		paginator.page_size = 10
		page = paginator.paginate_queryset(queryset, request)
		serializer = self.get_serializer(page, many=True)
		return paginator.get_paginated_response(serializer.data)
