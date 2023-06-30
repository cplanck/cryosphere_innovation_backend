from django.db.models import Q


def deployment_permissions_filter(self, queryset):
    deployment_objects = queryset
    if not self.request.user.is_authenticated:
        print('USER IS ANONOMOUS')
        print(self.request)
        deployments = deployment_objects.filter(private=False)

    elif self.request.user.is_staff:
        print('USER IS STAFF: ', self.request.user)
        print(self.request)
        print(self.request.META)
        print(self.request.COOKIES)
        # print('TOTAL QUERYSETS PASSED INTO PERSMISSIONS FILTER', queryset.count())
        deployments = deployment_objects
        # print('TOTAL DEPLOYMENT QUERYSETS: ', deployments.count())
        # print('TOTAL DEPLOYMENT OBJECTS: ', deployment_objects.count())

    elif self.request.user.is_authenticated:
        print('USER IS REGULAR USER: ', self.request.user)
        deployments = deployment_objects.exclude(
            Q(private=True) & ~(
                Q(instrument__owner=self.request.user) | Q(
                    collaborators=self.request.user)
            )
        )
    else:
        deployments = deployment_objects.filter(
            instrument__internal=True).filter(private=False)

    # print(self.request.user)
    # print(deployments)
    return deployments
