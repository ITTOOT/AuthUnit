from django.contrib.auth import get_user_model
from django.db import IntegrityError

from core.models.userModels import UserLoginLog, UserProfile, UserRanking, UserRating, Affiliation
from core.models.utilityModels import AppSettings
from core.serializers.userSerializers import UserLoginLogSerializer, UserSerializer, UserProfileSerializer, \
    RankingSerializer, RatingSerializer, AffiliationSerializer
from django.shortcuts import get_object_or_404

User = get_user_model()

# Login
class UserLoginLogService:
    @staticmethod
    def list(self, user_id):
        return UserLoginLog.objects.filter(user_id=user_id)

    @staticmethod
    def create(data):
        serializer = UserLoginLogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return None

    @staticmethod
    def update(user_login_log, data):
        serializer = UserLoginLogSerializer(user_login_log, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return None

    @staticmethod
    def delete(user_login_log):
        user_login_log.delete()


# User
class UserService:
    @staticmethod
    def get_by_id(user_id):
        return get_object_or_404(User, id=user_id)

    @staticmethod
    def list():
        return User.objects.all()

    @staticmethod
    def create(data):
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return None

    @staticmethod
    def update(user, data):
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return None

    @staticmethod
    def delete(user):
        user.delete()


# Profile
class UserProfileService:
    @staticmethod
    def list():
        return UserProfile.objects.all()

    @staticmethod
    def create(data):
        serializer = UserProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return None

    @staticmethod
    def update(user_profile, data):
        serializer = UserProfileSerializer(user_profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return None

    @staticmethod
    def delete(user_profile):
        user_profile.delete()


# Ranking
class RankingService:
    @staticmethod
    def list():
        return UserRanking.objects.all()

    @staticmethod
    def create(data):
        serializer = RankingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return None

    @staticmethod
    def update(ranking, data):
        serializer = RankingSerializer(ranking, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return None

    @staticmethod
    def delete(ranking):
        ranking.delete()


# Rating
class RatingService:
    @staticmethod
    def list():
        return UserRating.objects.all()

    @staticmethod
    def create(data):
        serializer = RatingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return None

    @staticmethod
    def update(rating, data):
        serializer = RatingSerializer(rating, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return None

    @staticmethod
    def delete(rating):
        rating.delete()


# Affiliation
class AffiliationService:
    @staticmethod
    def list():
        return Affiliation.objects.all()

    @staticmethod
    def create(data):
        serializer = AffiliationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return None

    @staticmethod
    def update(affiliation, data):
        serializer = AffiliationSerializer(affiliation, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return None

    @staticmethod
    def delete(affiliation):
        affiliation.delete()


# User Utility
class UserUtilityService:
    @staticmethod
    def create_user(username, password, email):
        try:
            # Create the user
            user = User.objects.create_user(username=username, password=password, email=email)

            # Create related objects
            profile = UserProfile.objects.create(user=user)
            settings = AppSettings.objects.create(user=user)

            # Update user fields
            user.profile = profile
            user.settings = settings
            user.save()

            return user
        except IntegrityError:
            raise ValueError('Username already exists. Please register with a different username.')
        except Exception as e:
            raise ValueError(str(e))

    @staticmethod
    def list():
        return User.objects.all()

    @staticmethod
    def get_by_id(user_id):
        return User.objects.get(id=user_id)

    @staticmethod
    def delete_user(user):
        user.delete()

    @staticmethod
    def save(user):
        return user.save()

