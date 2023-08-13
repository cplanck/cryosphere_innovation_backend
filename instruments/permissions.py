from rest_framework.permissions import BasePermission
from rest_framework import permissions

class CheckDeploymentReadWritePermissions(BasePermission):

    """
    Object-level permission checking for deployment instances. 

    The Cryosphere deployment access model needs to accomodate several access cases:

    - Public deployments need un-authenticated read-access (for public viewing on the website)
    - Private deployments need authenticated access granted only to instrument owners and collaborators
    - Public and private deployments need write access only for owners, collaborators, and staff

    This class checks if user has access to the deployment by the following rules:
    -If user is staff, always return True
    -If deployment is private, return True only if user is owner or collaborator (both have FULL read/write access)
    -If deployment is not private and request.method is safe, return True (let anyone make a GET request)
    -If not private but request is not safe, only allow owners and collaborators 

    Written 11 August 2023
    """

    def has_object_permission(self, request, view, obj):
        """
        Given a deployment object, run permissions depending on the user and deployment settings
        """
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
    