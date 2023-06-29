from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from ratelimit.decorators import ratelimit
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from core.serializers.utilitySerializers import AppSettingsSerializer
from core.services.adminServices import AppSettingsService
from rest_framework.response import Response
from django.middleware.csrf import get_token
from core.security.customPermissions import AdminPermission


# App Settings View
class AppSettingsViewSet(APIView):
    permission_classes = [AllowAny]
    service = AppSettingsService()
    serializer_class = AppSettingsSerializer

    @method_decorator(cache_page(60 * 15)) # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def get(self, request):
        settings = self.service.list()
        serializer = self.serializer_class(settings, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 15)) # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def post(self, request):
        data = request.data
        data = self.service.create(data)
        serializer = self.serializer_class(data)
        if isinstance(data, dict):
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    def put(self, request, pk=None):
        instance = self.service.list()
        data = request.data
        data = self.service.update(instance, data)
        serializer = self.serializer_class(data)
        if isinstance(data, dict):
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        instance = self.service.list()
        self.service.delete(instance)
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