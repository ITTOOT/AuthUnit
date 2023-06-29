from django.db import models
from django.contrib.auth import get_user_model


# App Settings
class AppSettings(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        default=None,
        related_name='app_settings'
    )
    webdriver_location = models.CharField(max_length=255)
    logging_file_location = models.CharField(max_length=255)

