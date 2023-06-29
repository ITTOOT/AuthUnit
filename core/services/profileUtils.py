from django.shortcuts import get_object_or_404
from core.models.userModels import UserProfile, UserPhoto
from core.serializers.userSerializers import UserProfileSerializer, UserPhotoSerializer


# User Profile Service
class UserProfileService:
    def get_by_id(self, user_id):
        return get_object_or_404(UserProfile, user_id=user_id)

    def get(self, user_id):
        profile = self.get_by_id(user_id)
        serializer = UserProfileSerializer(profile)
        return serializer.data

    def update(self, user_id, data):
        profile = self.get_by_id(user_id)
        serializer = UserProfileSerializer(profile, data=data)

        if serializer.is_valid():
            profile = serializer.save()
            return serializer.data
        return serializer.errors

    def delete(self, user_id):
        profile = self.get_by_id(user_id)
        profile.delete()


# User Photo Service
class UserPhotoService:
    def get_by_id(self, user_id):
        return get_object_or_404(UserPhoto, user_id=user_id)

    def get(self, user_id):
        photo = self.get_by_id(user_id)
        serializer = UserPhotoSerializer(photo)
        return serializer.data

    def update(self, user_id, data):
        photo = self.get_by_id(user_id)
        serializer = UserPhotoSerializer(photo, data=data)

        if serializer.is_valid():
            photo = serializer.save()
            return serializer.data
        return serializer.errors

    def delete(self, user_id):
        photo = self.get_by_id(user_id)
        photo.delete()


