from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ReviewViewSet, RegisterView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]
