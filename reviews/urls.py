from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ReviewViewSet, RegisterView, UserProfileViewSet, 
    ReviewLikeViewSet, ReviewCommentViewSet, search_movies_view, 
    movie_details_view, movie_info_view
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'reviews', ReviewViewSet)
router.register(r'likes', ReviewLikeViewSet, basename='like')
router.register(r'comments', ReviewCommentViewSet, basename='comment')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('search-movies/', search_movies_view, name='search-movies'),
    path('movie-details/<str:imdb_id>/', movie_details_view, name='movie-details'),
    path('movie-info/', movie_info_view, name='movie-info'),
    path('', include(router.urls)),
]
