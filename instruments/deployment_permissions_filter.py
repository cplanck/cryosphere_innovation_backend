from django.db.models import Q


def deployment_permissions_filter(self, queryset):
    deployment_objects = queryset
    if not self.request.user.is_authenticated:
        deployments = deployment_objects.filter(private=False)
    elif self.request.user.is_staff:
        deployments = deployment_objects
    elif self.request.user.is_authenticated:
        deployments = deployment_objects.exclude(
            Q(private=True) & ~(
                Q(instrument__owner=self.request.user) | Q(
                    collaborators=self.request.user)
            )
        )
    else:
        deployments = deployment_objects.filter(private=False)
    return deployments
