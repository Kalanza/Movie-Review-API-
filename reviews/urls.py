from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ReviewViewSet, RegisterView, UserProfileViewSet, ReviewLikeViewSet, ReviewCommentViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'reviews', ReviewViewSet)
router.register(r'likes', ReviewLikeViewSet, basename='like')
router.register(r'comments', ReviewCommentViewSet, basename='comment')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]
