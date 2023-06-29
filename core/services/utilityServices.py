from django.db import IntegrityError
from core.serializers.userSerializers import FeedbackSerializer
from core.models.userModels import User, Feedback, UserProfile
from core.models.utilityModels import AppSettings
from django.shortcuts import get_object_or_404


# User Feedback
class FeedbackService:
    @staticmethod
    def get_by_id(feedback_id):
        return get_object_or_404(Feedback, id=feedback_id)

    @staticmethod
    def list():
        return Feedback.objects.all()

    @staticmethod
    def create(data, user):
        serializer = FeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return serializer.data
        raise Exception(serializer.errors)

    @staticmethod
    def delete(feedback):
        feedback.delete()



