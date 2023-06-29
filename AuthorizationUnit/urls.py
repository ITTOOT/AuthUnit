"""
URL configuration for AuthorizationUnit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from core.views.userViews import UserLoginLogView, UserRegistrationView, UserVerificationView
from core.views.profileViews import UserProfileDetailView, UserPhotoDetailView
from core.views.adminViews import AppSettingsViewSet
from core.views.utilityViews import FeedbackAPIView, log_file_view
from core.views.statsViews import UserStatisticsView
from core.views.homeView import home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('profile/<int:user_id>/', UserProfileDetailView.as_view(), name='user_profile_detail'),
    path('photo/<int:user_id>/', UserPhotoDetailView.as_view(), name='user_photo_detail'),
    path('verify/<int:user_id>/', UserVerificationView.as_view(), name='user_verification'),
    # path('user-login-logs/', UserLoginLogView.as_view(), name='user_login_logs'),
    path('user-login-logs/', UserLoginLogView.as_view(), name='user_login_logs'),
    path('user_login_logs/<int:log_id>/', UserLoginLogView.as_view(), name='user_login_logs'),
    path('app-settings/', AppSettingsViewSet.as_view(), name='app_settings'),
    # path('app-settings/', AppSettingsViewSet.as_view({'get': 'list'}), name='app_settings'),
    path('user-statistics/', UserStatisticsView.as_view(), name='user_statistics'),
    path('feedback/', FeedbackAPIView.as_view(), name='feedback'),
    path('log-file/<str:log_file_name>/', log_file_view, name='log_file'),
]
