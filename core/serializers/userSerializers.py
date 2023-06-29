from rest_framework import serializers
from core.models.userModels import UserLoginLog, User, UserProfile, \
    UserRanking, UserRating, Affiliation, UserPhoto, Feedback


# Login Log
class UserLoginLogSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserLoginLog
        fields = '__all__'

# User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# Profile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

# Picture
class UserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhoto
        fields = '__all__'

# Ranking
class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRanking
        fields = '__all__'

# Rating
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRating
        fields = '__all__'

# Affiliation
class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = '__all__'

# Feedback
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['user', 'message', 'created_at']