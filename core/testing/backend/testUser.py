from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse
from requests import Response
from rest_framework import status
from rest_framework.test import APIClient
from core.models.userModels import User, UserLoginLog, UserProfile, UserRanking, UserRating, Affiliation
from core.serializers.userSerializers import (
    UserLoginLogSerializer,
    UserSerializer,
    UserProfileSerializer,
    RankingSerializer,
    RatingSerializer,
    AffiliationSerializer,
)

# User = get_user_model()

# FIRST TESTS
class UserTestCase(TestCase):
    order = 1

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='test@example.com',
            password='password',
            auth_level='user',
            is_verified=True,
            user_type='individual',
            ip_address='127.0.0.1',
        )
        #self.profile = UserProfile.objects.create(user=self.user, first_name='Test', last_name='User')
        #self.ranking = UserRanking.objects.create(user_profile=self.profile, rank='9.5')
        #self.rating = UserRating.objects.create(user_profile=self.profile, rate='9.5')
        #self.affiliation = Affiliation.objects.create(user_profile=self.profile, affiliates='Test Affiliation')


    def test_user_creation(self):
        self.assertEqual(self.user.username, 'tester')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.auth_level, 'user')
        self.assertTrue(self.user.is_verified)
        self.assertEqual(self.user.user_type, 'individual')
        self.assertEqual(self.user.ip_address, '127.0.0.1')

    def test_user_str_representation(self):
        self.assertEqual(str(self.user), 'tester')


class UserProfileTestCase(TestCase):
    order = 2

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='test@example.com',
            password='password',
            auth_level='user',
            is_verified=True,
            user_type='individual',
            ip_address='127.0.0.1',
        )
        self.profile = UserProfile.objects.create(user=self.user, first_name='Test', last_name='User')

    def test_user_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.first_name, 'Test')
        self.assertEqual(self.profile.last_name, 'User')

    def test_user_profile_str_representation(self):
        expected_str = f"Profile ID {self.profile.id} = user ID {self.profile.user_id}"
        self.assertEqual(str(self.profile), expected_str)


class UserRankingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='test@example.com',
            password='password',
            auth_level='user',
            is_verified=True,
            user_type='individual',
            ip_address='127.0.0.1',
        )
        self.profile = UserProfile.objects.create(user=self.user, first_name='Test', last_name='User')
        self.ranking = UserRanking.objects.create(user_profile=self.profile, rank='9.5')

    def test_user_ranking_creation(self):
        self.assertEqual(self.ranking.user_profile, self.profile)
        self.assertEqual(self.ranking.rank, '9.5')

    def test_user_ranking_str_representation(self):
        expected_str = f"Ranking for UserProfile ID {self.profile.id} = {self.ranking.rank}"
        self.assertEqual(str(self.ranking), expected_str)

class UserRatingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='test@example.com',
            password='password',
            auth_level='user',
            is_verified=True,
            user_type='individual',
            ip_address='127.0.0.1',
        )
        self.profile = UserProfile.objects.create(user=self.user, first_name='Test', last_name='User')
        self.rating = UserRating.objects.create(user_profile=self.profile, rate='9.5')

    def test_user_rating_creation(self):
        self.assertEqual(self.rating.user_profile, self.profile)
        self.assertEqual(self.rating.rate, '9.5')

    def test_user_rating_str_representation(self):
        expected_str = f"Rating for UserProfile ID {self.profile.id} = {self.rating.rate}"
        self.assertEqual(str(self.rating), expected_str)


class AffiliationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='test@example.com',
            password='password',
            auth_level='user',
            is_verified=True,
            user_type='individual',
            ip_address='127.0.0.1',
        )
        self.profile = UserProfile.objects.create(user=self.user, first_name='Test', last_name='User')
        self.affiliation = Affiliation.objects.create(user_profile=self.profile, affiliates='Test Affiliation')

    def test_affiliation_creation(self):
        self.assertEqual(self.affiliation.user_profile, self.profile)
        self.assertEqual(self.affiliation.affiliates, 'Test Affiliation')

    def test_affiliation_str_representation(self):
        expected_str = f"Affiliation for UserProfile ID {self.profile.id} = {self.affiliation.affiliates}"
        self.assertEqual(str(self.affiliation), expected_str)


class UserLoginLogTestCase(TestCase):
    def setUp(self):
        # self.user = User.objects.create_user(
        #     username='tester',
        #     email='test@example.com',
        #     password='password',
        #     auth_level='user',
        #     is_verified=True,
        #     user_type='individual',
        #     ip_address='127.0.0.1',
        # )
        User = get_user_model()
        # Create a user record in auth_user table
        self.user = User.objects.create_user(username='example_user', password='password')
        self.login_log = UserLoginLog.objects.create(user=self.user, ip_address='127.0.0.1')

    def test_user_login_log_creation(self):
        self.assertEqual(UserLoginLog.objects.count(), 1)

    def test_user_login_log_str_representation(self):
        expected_str = str(self.user)
        self.assertEqual(str(self.login_log), expected_str)

    # def test_user_login_log_foreign_key_constraint(self):
    #     # Try to create a UserLoginLog with an invalid user_id
    #     invalid_user_id = 9999
    #     with self.assertRaises(ValidationError):
    #         UserLoginLog.objects.create(user_id=invalid_user_id, ip_address='127.0.0.1')


class UserLoginLogAPITestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='example_user', password='password')
        self.login_log = UserLoginLog.objects.create(user=self.user, ip_address='127.0.0.1')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def post(self, url, data=None, format=None, content_type=None, **extra):
        data = data.copy() if data else {}  # Create a mutable copy of the data
        data['user_id'] = self.user.id  # Add the user_id to the data dictionary
        format = format or 'json'  # Set default format to 'json' if not provided
        content_type = content_type or f'application/{format}'
        return self.client.generic('POST', url, data, format=format, content_type=content_type, **extra)

    def test_get_user_login_logs(self):
        url = reverse('user_login_logs')
        response = self.client.get(url)
        login_logs = UserLoginLog.objects.all()
        serializer = UserLoginLogSerializer(login_logs, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    # def test_create_user_login_log(self):
    #     url = reverse('user_login_logs')
    #     data = {
    #         "ip_address": "192.168.0.1",
    #     }
    #     response = self.post(url, data)
    #     print(response.data)  # Print response data for debugging
    #     print(response.status_code)  # Print response status code for debugging
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(UserLoginLog.objects.count(), 1)

    def delete(self, log_id):  # Update method signature to accept log_id
        user_login_log = get_object_or_404(UserLoginLog, pk=log_id)  # Use log_id parameter
        user_login_log.delete()  # Delete the user login log
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def test_delete_user_login_log(self):
    #     url = reverse('user_login_logs', args=[self.login_log.id])
    #     self.client.force_authenticate(user=self.user)  # Ensure user authentication
    #     response = self.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(UserLoginLog.objects.count(), 0)



