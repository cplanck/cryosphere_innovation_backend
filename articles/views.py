from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

import articles
from articles.models import Article
from articles.serializers import *
