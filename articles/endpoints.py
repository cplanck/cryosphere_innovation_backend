from rest_framework import pagination, status, viewsets
from rest_framework.response import Response

from articles.models import *
from articles.serializers import *


class ArticlePagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class ArticleEndpoint(viewsets.ModelViewSet):
    pagination_class = ArticlePagination
    queryset = Article.objects.all().order_by('-published_date')
    serializer_class = ArticleDetailSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        elif self.action == 'retrieve':
            return ArticleDetailSerializer
        else:
            return super().get_serializer_class()

    def get_object(self):
        slug = self.kwargs['pk']
        queryset = self.get_queryset()
        obj = queryset.filter(slug=slug).first()
        return obj
