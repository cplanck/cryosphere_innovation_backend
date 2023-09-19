import algoliasearch_django as algoliasearch
from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from documentation.models import Document

from .models import Deployment, Instrument
from .serializers import *


@register(Deployment)
class DeploymentModelIndex(AlgoliaIndex):

    """
    Run python3 manage.py algolia_reindex when you make changes to this file
    """

    fields = ('id', 'name', 'instrument', 'status', 'details',
              'deployment_start_date', 'deployment_end_date', 'location', 'algolia_index', 'path', 'data_uuid', 'slug', 'searchable', 'private')

    settings = {
        'searchableAttributes': ['algolia_index', 'status', 'deployment_start_date', 'deployment_end_date', 'location', 'details', 'path'],
        'attributesForFaceting': ['status'],
        'allowTyposOnNumericTokens': False,
        'customRanking': ['asc(status)']
    }

    def get_queryset(self):
        queryset = Deployment.objects.exclude(private=True).exclude(searchable=False)
        return queryset

@register(Document)
class DocumentModelIndex(AlgoliaIndex):

    """
    Run python3 manage.py algolia_reindex when you make changes to this file
    """

    def get_queryset(self):
        queryset = Document.objects.filter(status='Published')
        return queryset
