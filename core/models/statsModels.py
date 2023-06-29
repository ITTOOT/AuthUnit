from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


# User statistics - to be expanded
class UserStatistics(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_statistics')
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField()
    login_location = models.CharField(max_length=255)
    page_visits = models.IntegerField()

    class Meta:
        verbose_name_plural = "User Statistics"



