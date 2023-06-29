from core.models.utilityModels import AppSettings
from core.serializers.utilitySerializers import AppSettingsSerializer
from core.models.userModels import User
from django.shortcuts import get_object_or_404

# App Settings Service
class AppSettingsService:
    @staticmethod
    def get_by_id(user_id):
        return get_object_or_404(User, id=user_id)

    @staticmethod
    def list():
        return AppSettings.objects.all()

    @staticmethod
    def create(data):
        serializer = AppSettingsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return None

    @staticmethod
    def update(instance, data):
        serializer = AppSettingsSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return None

    @staticmethod
    def delete(instance):
        instance.delete()


