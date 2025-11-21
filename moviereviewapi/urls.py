"""
URL configuration for moviereviewapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse
from django.utils import timezone
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# drf-yasg imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

def api_root(request):
    """Root API endpoint with available endpoints"""
    return JsonResponse({
        'message': 'Welcome to Movie Review API',
        'version': 'v1',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'authentication': {
                'token': '/api/token/',
                'refresh': '/api/token/refresh/',
            },
            'documentation': {
                'swagger': '/swagger/',
                'redoc': '/redoc/',
            }
        }
    })

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create a custom schema view that bypasses all authentication
@method_decorator(csrf_exempt, name='dispatch')
class PublicSchemaView(get_schema_view(
    openapi.Info(
        title="Movie Review API",
        default_version='v1',
        description="API documentation for the Movie Review project",
    ),
    public=True,
    permission_classes=(),
    authentication_classes=(),
)):
    pass

# Create instances for different formats
schema_view_json = PublicSchemaView.as_view()
schema_view_swagger = PublicSchemaView.as_view()
schema_view_redoc = PublicSchemaView.as_view()

def test_view(request):
    """Simple test view to check if anonymous access works"""
    return JsonResponse({'message': 'Anonymous access works!', 'timestamp': str(timezone.now())})

urlpatterns = [
    # API Documentation (put these first to avoid conflicts)
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', 
            schema_view_json, 
            name='schema-json'),
    re_path(r'^swagger/$', 
            schema_view_swagger, 
            name='schema-swagger-ui'),
    re_path(r'^redoc/$', 
            schema_view_redoc, 
            name='schema-redoc'),
    
    # Test endpoint
    path('test/', test_view, name='test'),
    
    # Django Allauth URLs
    path('accounts/', include('allauth.urls')),
    
    # Web Interface (Home page)
    path('', include('reviews.urls')),  # This will handle both web and API routes
    
    # Admin
    path("admin/", admin.site.urls),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
