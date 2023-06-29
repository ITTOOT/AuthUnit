from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission, AllowAny
from ratelimit.decorators import ratelimit
from rest_framework.views import APIView
from core.models.userModels import User, UserLoginLog, Affiliation, UserRating, UserRanking, UserProfile
from core.serializers.userSerializers import UserLoginLogSerializer, UserSerializer, UserProfileSerializer, \
    RankingSerializer, RatingSerializer, AffiliationSerializer
from core.services.userServices import UserLoginLogService, UserProfileService, RankingService, RatingService, \
    AffiliationService, UserService, UserUtilityService
from django.middleware.csrf import get_token
from core.security.customPermissions import AdminPermission


# User Login
class UserLoginLogView(APIView):
    permission_classes = [IsAuthenticated]
    service = UserLoginLogService()

    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def get(self, request):
        user_login_logs = self.service.list(self, user_id=request.user.id)
        serializer = UserLoginLogSerializer(user_login_logs, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def post(self, request):
        data = request.data.copy()  # Create a copy of the data dictionary
        data['user_id'] = request.user.id
        created_user_login_log = self.service.create(data)
        if created_user_login_log is not None:  # Check if create method returned a valid log
            return Response(created_user_login_log, status=status.HTTP_201_CREATED)
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        user_login_log = get_object_or_404(UserLoginLog, pk=pk)
        data = request.data
        updated_user_login_log = self.service.update(user_login_log, data)
        if updated_user_login_log:
            return Response(updated_user_login_log, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_login_log = get_object_or_404(UserLoginLog, pk=pk)
        self.service.delete(user_login_log)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # In function-based views, the dispatch process is handled implicitly by
    # the Django view system, whereas in class-based views, the dispatch
    # method explicitly handles the dispatch process.
    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        # Set the CSRF token in the response headers
        response = super().dispatch(request, *args, **kwargs)
        response['X-CSRFToken'] = get_token(request)
        return response


# User
class UserView(APIView):
    permission_classes = [IsAdminUser]
    service = UserService()

    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def get_by_id(self, request):
        user_id = request.user.id
        user = self.service.get_by_id(user_id)

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def get(self, request):
        users = self.service.list()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def post(self, request):
        data = request.data
        created_user = self.service.create(data)
        if created_user:
            return Response(created_user, status=status.HTTP_201_CREATED)
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        data = request.data
        updated_user = self.service.update(user, data)
        if updated_user:
            return Response(updated_user, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.service.delete(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # In function-based views, the dispatch process is handled implicitly by
    # the Django view system, whereas in class-based views, the dispatch
    # method explicitly handles the dispatch process.
    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        # Set the CSRF token in the response headers
        response = super().dispatch(request, *args, **kwargs)
        response['X-CSRFToken'] = get_token(request)
        return response


# Profile
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    service = UserProfileService()

    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def get(self, request):
        user_profiles = self.service.list()
        serializer = UserProfileSerializer(user_profiles, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def post(self, request):
        data = request.data
        created_user_profile = self.service.create(data)
        if created_user_profile:
            return Response(created_user_profile, status=status.HTTP_201_CREATED)
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        user_profile = get_object_or_404(UserProfile, pk=pk)
        data = request.data
        updated_user_profile = self.service.update(user_profile, data)
        if updated_user_profile:
            return Response(updated_user_profile, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_profile = get_object_or_404(UserProfile, pk=pk)
        self.service.delete(user_profile)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # In function-based views, the dispatch process is handled implicitly by
    # the Django view system, whereas in class-based views, the dispatch
    # method explicitly handles the dispatch process.
    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        # Set the CSRF token in the response headers
        response = super().dispatch(request, *args, **kwargs)
        response['X-CSRFToken'] = get_token(request)
        return response


# Ranking
class RankingView(APIView):
    permission_classes = [IsAdminUser]
    service = RankingService()

    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def get(self, request):
        rankings = self.service.list()
        serializer = RankingSerializer(rankings, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def post(self, request):
        data = request.data
        created_ranking = self.service.create(data)
        if created_ranking:
            return Response(created_ranking, status=status.HTTP_201_CREATED)
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        ranking = get_object_or_404(UserRanking, pk=pk)
        data = request.data
        updated_ranking = self.service.update(ranking, data)
        if updated_ranking:
            return Response(updated_ranking, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ranking = get_object_or_404(UserRanking, pk=pk)
        self.service.delete(ranking)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # In function-based views, the dispatch process is handled implicitly by
    # the Django view system, whereas in class-based views, the dispatch
    # method explicitly handles the dispatch process.
    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        # Set the CSRF token in the response headers
        response = super().dispatch(request, *args, **kwargs)
        response['X-CSRFToken'] = get_token(request)
        return response


# Rating
class RatingView(APIView):
    permission_classes = [IsAdminUser]
    service = RatingService()

    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def get(self, request):
        ratings = self.service.list()
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def post(self, request):
        data = request.data
        created_rating = self.service.create(data)
        if created_rating:
            return Response(created_rating, status=status.HTTP_201_CREATED)
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        rating = get_object_or_404(UserRating, pk=pk)
        data = request.data
        updated_rating = self.service.update(rating, data)
        if updated_rating:
            return Response(updated_rating, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        rating = get_object_or_404(UserRating, pk=pk)
        self.service.delete(rating)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # In function-based views, the dispatch process is handled implicitly by
    # the Django view system, whereas in class-based views, the dispatch
    # method explicitly handles the dispatch process.
    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        # Set the CSRF token in the response headers
        response = super().dispatch(request, *args, **kwargs)
        response['X-CSRFToken'] = get_token(request)
        return response


# Affiliation
class AffiliationView(APIView):
    permission_classes = [IsAuthenticated]
    service = AffiliationService()

    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def get(self, request):
        affiliations = self.service.list()
        serializer = AffiliationSerializer(affiliations, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def post(self, request):
        data = request.data
        created_affiliation = self.service.create(data)
        if created_affiliation:
            return Response(created_affiliation, status=status.HTTP_201_CREATED)
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        affiliation = get_object_or_404(Affiliation, pk=pk)
        data = request.data
        updated_affiliation = self.service.update(affiliation, data)
        if updated_affiliation:
            return Response(updated_affiliation, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        affiliation = get_object_or_404(Affiliation, pk=pk)
        self.service.delete(affiliation)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # In function-based views, the dispatch process is handled implicitly by
    # the Django view system, whereas in class-based views, the dispatch
    # method explicitly handles the dispatch process.
    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        # Set the CSRF token in the response headers
        response = super().dispatch(request, *args, **kwargs)
        response['X-CSRFToken'] = get_token(request)
        return response



# User Registration
class UserRegistrationView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    service = UserUtilityService()
    queryset = User.objects.all()

    # @method_decorator(AdminPermission)  # Require authentication for this view
    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def get(self, request):
        users = self.service.list()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = make_password(data.get('password'))  # PBKDF2
        email = data.get('email')

        if not username or not password or not email:
            return Response({'error': 'Please provide all required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = self.service.create_user(username=username, password=password, email=email)
            return Response({'success': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, user_id):
        user = self.service.get_by_id(user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = self.service.get_by_id(user_id)
        self.service.delete_user(user)
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


# User Verification
class UserVerificationView(APIView):
    permission_classes = [AdminPermission, AllowAny]
    #permission_classes = [AllowAny]
    service = UserUtilityService()

    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def get(self, request):
        user_id = request.user.id
        user = self.service.get_by_id(user_id)

        user.is_verified = True
        self.service.save(user)

        return redirect('verification_success')

    @method_decorator(cache_page(60 * 15))  # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def post(self, request):
        users = self.service.list()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def put(self, request, user_id):
        user = self.service.get_by_id(user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = self.service.get_by_id(user_id)
        self.service.delete_user(user)
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


# EXAMPLE
@csrf_protect
@ratelimit(key='user_or_ip', rate='100/h', block=True)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protectedView(request):
    # Only authenticated users will have access to this view
    return Response({'message': 'This is a protected view'})

