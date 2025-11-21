from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ReviewViewSet, RegisterView, UserProfileViewSet, 
    ReviewLikeViewSet, ReviewCommentViewSet, search_movies_view, 
    movie_details_view, movie_info_view, home_view, movie_search_view,
    ReviewsListView, search_movies_public, review_detail_view
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'reviews', ReviewViewSet)
router.register(r'likes', ReviewLikeViewSet, basename='like')
router.register(r'comments', ReviewCommentViewSet, basename='comment')

urlpatterns = [
    # Web Interface URLs
    path('', home_view, name='home'),
    path('search/', movie_search_view, name='movie_search'),
    path('reviews/', ReviewsListView.as_view(), name='reviews_list'),
    path('reviews/<int:pk>/', review_detail_view, name='review_detail'),
    
    # API URLs
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/search-movies/', search_movies_public, name='search-movies-public'),
    path('api/search-movies-auth/', search_movies_view, name='search-movies'),
    path('api/movie-details/<str:imdb_id>/', movie_details_view, name='movie-details'),
    path('api/movie-info/', movie_info_view, name='movie-info'),
    path('api/', include(router.urls)),
]
