# from django.contrib.auth import get_user_model
#from django.db import models
#from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager, Group, Permission
from django.db import models
#from core.models.userModels import User
# You can retrieve the statistics for a particular user by accessing the user_statistics attribute
# on a User instance. For example, if you have a user object, you can access their statistics using
# user.user_statistics.all(). Similarly, you can access other related objects using the appropriate
# attributes (e.g., user.login_logs.all(), user.profile, etc.).

# User
class UserManager(DefaultUserManager):
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    AUTH_LEVELS = (
        ('admin', 'Admin'),
        ('engineer', 'Engineer'),
        ('manager', 'Manager'),
        ('supervisor', 'Supervisor'),
        ('user', 'User'),
        ('applicant', 'Applicant'),
    )

    USER_TYPES = (
        ('individual', 'Individual'),
        ('group', 'Group'),
        ('organisation', 'Organisation'),
        ('charity', 'Charity'),
        ('government', 'Government'),
    )

    auth_level = models.CharField(max_length=50, choices=AUTH_LEVELS, default='applicant')
    is_verified = models.BooleanField(default=False)
    user_type = models.CharField(max_length=50, choices=USER_TYPES, default='individual')
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    objects = UserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        related_query_name='custom_user',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        related_query_name='custom_user',
        blank=True,
    )

# Login Log
class UserLoginLog(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=255)
    # ip_address = models.GenericIPAddressField()
    login_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'User Login Logs'

    def __str__(self):
        return str(self.user)

# User Profile
# UserProfile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    aliases = models.TextField(blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    addresses = models.JSONField(default=list)
    email_address = models.EmailField()
    description = models.TextField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    verification = models.BooleanField(default=False)
    statistics = models.ManyToManyField('UserStatistics', related_name='users')
    #
    def __str__(self):
        return f'Profile ID {self.id} = user ID {self.user_id}'

# UserRanking
class UserRanking(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='rankings')
    rank = models.CharField(max_length=255)
    # Other fields related to rankings
    def __str__(self):
        return f'Ranking for UserProfile ID {self.user_profile_id} = {self.rank}'

# UserRating
class UserRating(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings')
    rate = models.DecimalField(max_digits=3, decimal_places=2)
    # Other fields related to ratings
    def __str__(self):
        return f'Rating for UserProfile ID {self.user_profile_id} = {self.rate}'

# Affiliation
class Affiliation(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='affiliations')
    affiliates = models.CharField(max_length=255)
    # Other fields related to affiliations
    def __str__(self):
        return f'Affiliation for UserProfile ID {self.user_profile_id} = {self.affiliates}'



# User Pictures
class UserPhoto(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='photo')
    photo = models.ImageField(upload_to='user_photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'User Photos'

    def __str__(self):
        return f"Photo for {self.user.username}, ID {self.user.id}"


# User Feedback
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

