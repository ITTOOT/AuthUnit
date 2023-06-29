from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_protect
from core.services.profileUtils import UserProfileService, UserPhotoService
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token
from core.security.customPermissions import AdminPermission

# Get the Auth User
User = get_user_model()

# User Profile View
class UserProfileDetailView(APIView):
    permission_classes = [AllowAny]
    service = UserProfileService()

    @method_decorator(cache_page(60 * 15)) # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def get(self, request, user_id):
        data = self.service.get(user_id)
        return Response(data)

    def put(self, request, user_id):
        data = request.data
        data = self.service.update(user_id, data)
        if isinstance(data, dict):
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data)

    def delete(self, request, user_id):
        self.service.delete(user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # In function-based views, the dispatch process is handled implicitly by
    # the Django view system, whereas in class-based views, the dispatch
    # method explicitly handles the dispatch process.
    @method_decorator(cache_page(60 * 15)) # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        # Set the CSRF token in the response headers
        response = super().dispatch(request, *args, **kwargs)
        response['X-CSRFToken'] = get_token(request)
        return response


# User Photo View
class UserPhotoDetailView(APIView):
    permission_classes = [AllowAny]
    service = UserPhotoService()

    @method_decorator(cache_page(60 * 15)) # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def get(self, request, user_id):
        data = self.service.get(user_id)
        return Response(data)

    def put(self, request, user_id):
        data = request.data
        data = self.service.update(user_id, data)
        if isinstance(data, dict):
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data)

    def delete(self, request, user_id):
        self.service.delete(user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # In function-based views, the dispatch process is handled implicitly by
    # the Django view system, whereas in class-based views, the dispatch
    # method explicitly handles the dispatch process.
    @method_decorator(cache_page(60 * 15)) # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        # Set the CSRF token in the response headers
        response = super().dispatch(request, *args, **kwargs)
        response['X-CSRFToken'] = get_token(request)
        return response

