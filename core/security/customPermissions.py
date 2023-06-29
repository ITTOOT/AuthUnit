from rest_framework.permissions import BasePermission


# Permissions - only named user can access
# Admin
class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'admin'


# User
class UserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ['admin', 'user']


# Engineer
class EngineerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ['admin', 'engineer']


# Manager
class ManagerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ['admin', 'manager']


# Supervisor
class SupervisorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ['admin', 'supervisor']


# Applicant
class ApplicantPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ['admin', 'applicant']

