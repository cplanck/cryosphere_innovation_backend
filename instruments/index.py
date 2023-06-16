import algoliasearch_django as algoliasearch
from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from articles.models import Article

from .models import Deployment, Instrument
from .serializers import *


@register(Deployment)
class DeploymentModelIndex(AlgoliaIndex):

    fields = ('id', 'name', 'instrument', 'status', 'details',
              'deployment_start_date', 'deployment_end_date', 'location', 'algolia_index', 'path')

    settings = {
        'searchableAttributes': ['algolia_index', 'status', 'deployment_start_date', 'deployment_end_date', 'location', 'details', 'path']
    }

    def get_queryset(self):
        queryset = Deployment.objects.exclude(private=True)
        return queryset


algoliasearch.register(Instrument)
algoliasearch.register(Article)
