import os

from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.views.decorators.cache import cache_page
from ratelimit.decorators import ratelimit
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.serializers.userSerializers import FeedbackSerializer, UserSerializer
from django.contrib.auth.hashers import make_password
from core.services.utilityServices import FeedbackService
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from core.security.customPermissions import AdminPermission
from core.testing.testRunner import PROJECT_ROOT

# Get the Auth User
User = get_user_model()


# User Feedback
class FeedbackAPIView(APIView):
    permission_classes = [AllowAny]
    service = FeedbackService()

    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def get(self, request):
        feedbacks = self.service.list()
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def post(self, request):
        data = request.data
        user = request.user
        try:
            feedback_data = self.service.create(data, user)
            return Response(feedback_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, feedback_id):
        feedback = self.service.get_by_id(feedback_id)
        serializer = FeedbackSerializer(feedback, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, feedback_id):
        feedback = self.service.get_by_id(feedback_id)
        self.service.delete(feedback)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # In function-based views, the dispatch process is handled implicitly by
    # the Django view system, whereas in class-based views, the dispatch
    # method explicitly handles the dispatch process
    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        # Set the CSRF token in the response headers
        response = super().dispatch(request, *args, **kwargs)
        response['X-CSRFToken'] = get_token(request)
        return response


# Set the path to the log file
LOG_DIR = os.path.join(PROJECT_ROOT, 'core', 'testing', 'backend', 'logs')

# Log file access
def log_file_view(request, log_file_name):
    if request.user.is_superuser:
        try:
            log_file_path = os.path.join(LOG_DIR, log_file_name)
            with open(log_file_path, 'r') as log_file:
                log_content = log_file.read()
            return HttpResponse(log_content, content_type='text/plain')
        except FileNotFoundError:
            return HttpResponse('Log file not found', status=404)
    else:
        return HttpResponse('You do not have permission to access the log file', status=403)

