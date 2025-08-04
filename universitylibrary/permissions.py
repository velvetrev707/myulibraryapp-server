from rest_framework import permissions

class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request)
        print(f"Checking if user is authenticated and is a librarian %s and %s", (request.user.is_authenticated, request.user.user_type))
        return request.user.is_authenticated and request.user.user_type == 'librarian'

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'student'