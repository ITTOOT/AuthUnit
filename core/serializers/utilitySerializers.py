from rest_framework import serializers
from core.models.utilityModels import AppSettings


# Settings
class AppSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppSettings
        fields = ['webdriver_location', 'logging_file_location']

