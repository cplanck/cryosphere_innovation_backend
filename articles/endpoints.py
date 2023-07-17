from authentication.http_cookie_authentication import CookieTokenAuthentication
from rest_framework import pagination, status, viewsets
from rest_framework.response import Response

from articles.models import *
from articles.serializers import *


class ArticlePagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class ArticleEndpoint(viewsets.ModelViewSet):
    authentication_classes = [CookieTokenAuthentication]
    pagination_class = ArticlePagination
    queryset = Article.objects.all().order_by('-published_date')
    serializer_class = ArticleDetailSerializer
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        elif self.action == 'retrieve':
            return ArticleDetailSerializer
        else:
            return super().get_serializer_class()

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        else:
            return self.queryset.filter(status='Published')


class ArticleImageEndpoint(viewsets.ModelViewSet):
    queryset = ArticleImages.objects.all()
    serializer_class = ArticleImageSerializer

    def create(self, request):
        print(request.FILES['file'])

        image = ArticleImages(location=request.FILES['file'])
        image.save()
        file_url = image.location.url

        return Response({'location': file_url}, status=status.HTTP_201_CREATED)
