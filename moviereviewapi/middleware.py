from django.contrib.auth.middleware import AuthenticationMiddleware
from django.urls import resolve


class SkipAuthenticationForSwaggerMiddleware:
    """
    Custom middleware that skips Django authentication for swagger documentation URLs.
    This allows anonymous access to API documentation while maintaining authentication
    for other parts of the application.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Store the original authentication middleware
        self.auth_middleware = AuthenticationMiddleware(get_response)

    def __call__(self, request):
        # Check if the request is for swagger documentation
        if self._is_swagger_url(request.path):
            # For swagger URLs, skip authentication by setting user to AnonymousUser
            from django.contrib.auth.models import AnonymousUser
            request.user = AnonymousUser()
            # Call the next middleware without authentication
            return self.get_response(request)
        else:
            # For all other URLs, use normal authentication
            return self.auth_middleware(request)

    def _is_swagger_url(self, path):
        """Check if the path is a swagger documentation URL"""
        swagger_paths = [
            '/swagger/',
            '/swagger.json',
            '/swagger.yaml',
            '/redoc/',
            '/test/',  # Also allow our test endpoint
        ]
        return any(path.startswith(swagger_path) for swagger_path in swagger_paths)