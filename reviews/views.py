from .omdb_utils import fetch_movie_info, search_movies, fetch_movie_by_imdb_id
from rest_framework import viewsets, permissions, filters, generics
from django.contrib.auth.models import User
from .models import Review, UserProfile, ReviewLike, ReviewComment
from .serializers import UserSerializer, ReviewSerializer, UserProfileSerializer, ReviewLikeSerializer, ReviewCommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse

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

# OMDB API endpoints
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_movies_view(request):
    """
    Search for movies using OMDB API
    Example: /api/search-movies/?q=inception
    """
    query = request.GET.get('q', '')
    if not query:
        return Response({'error': 'Query parameter q is required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    movies = search_movies(query)
    if movies is not None:
        return Response({'movies': movies}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'No movies found or API error'}, 
                       status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_details_view(request, imdb_id):
    """
    Get detailed movie information by IMDB ID
    Example: /api/movie-details/tt3896198/
    """
    movie_info = fetch_movie_by_imdb_id(imdb_id)
    if movie_info:
        return Response(movie_info, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Movie not found'}, 
                       status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_info_view(request):
    """
    Get movie information by title
    Example: /api/movie-info/?title=inception
    """
    title = request.GET.get('title', '')
    if not title:
        return Response({'error': 'Title parameter is required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    movie_info = fetch_movie_info(title)
    if movie_info:
        return Response(movie_info, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Movie not found'}, 
                       status=status.HTTP_404_NOT_FOUND)

# Template Views for Web Interface
def home_view(request):
    """Home page with recent reviews"""
    recent_reviews = Review.objects.order_by('-created_date')[:6]
    return render(request, 'reviews/home.html', {
        'recent_reviews': recent_reviews
    })

def movie_search_view(request):
    """Movie search page"""
    return render(request, 'reviews/movie_search.html')

class ReviewsListView(ListView):
    """Reviews list page with pagination"""
    model = Review
    template_name = 'reviews/reviews_list.html'
    context_object_name = 'reviews'
    paginate_by = 12
    ordering = ['-created_date']

# API endpoint for the frontend search (without authentication)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_movies_public(request):
    """
    Public search endpoint for the web interface
    """
    query = request.GET.get('search', '')
    if not query:
        return Response({'error': 'Search parameter is required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    movies = search_movies(query)
    if movies is not None:
        return Response(movies, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'No movies found or API error'}, 
                       status=status.HTTP_404_NOT_FOUND)
