from authentication.http_cookie_authentication import CookieTokenAuthentication
from rest_framework import pagination, status, viewsets
from rest_framework.response import Response

from documentation.models import *
from documentation.serializers import *


class DocumentPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class DocumentEndpoint(viewsets.ModelViewSet):
    authentication_classes = [CookieTokenAuthentication]
    pagination_class = DocumentPagination
    queryset = Document.objects.all().order_by('-published_date')
    serializer_class = DocumentDetailSerializer
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return DocumentSerializer
        elif self.action == 'retrieve':
            return DocumentDetailSerializer
        else:
            return super().get_serializer_class()

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        else:
            return self.queryset.filter(status='Published')


class DocumentImageEndpoint(viewsets.ModelViewSet):
    queryset = DocumentImages.objects.all()
    serializer_class = DocumentImageSerializer

    def create(self, request):

        image = DocumentImages(location=request.FILES['file'])
        image.save()
        file_url = image.location.url

        return Response({'location': file_url}, status=status.HTTP_201_CREATED)
