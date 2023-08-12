from rest_framework.permissions import BasePermission
from rest_framework import permissions

class CheckDeploymentReadWritePermissions(BasePermission):
    """
    Object-level permission checking for deployment instances. 
    Checks if user has access to the deployment by the following rules:
    -If user is staff, always return True
    -If deployment is private, return True only if user is owner or collaborator (both have FULL read/write access)
    -If deployment is not private and request.method is safe, return True (let anyone make a GET request)
    -If not private but request is no-read, only allow owners and collaborators
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            # staff can do anything
            return True
        elif obj.private:
            # if private, only ever allow owners and collaborators to do anything
            return obj.instrument.owner == request.user or request.user in obj.collaborators.all()
        elif not obj.private and request.method in permissions.SAFE_METHODS:
            # if not private, let anyone make a GET request
            return True
        elif request.method not in permissions.SAFE_METHODS:
            # if not private but request is non-read, only allow owners and collaborators
            return obj.instrument.owner == request.user or request.user in obj.collaborators.all()
        return False