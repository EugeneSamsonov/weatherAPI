from datetime import datetime
from django.shortcuts import render
from django.core.cache import cache

from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from history.models import UserHistory
from history.pagination import HistoryResultsSetPagination
from history.serializers import UserHistorySerializer


# Create your views here.
class UserHistoryViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):

    serializer_class = UserHistorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HistoryResultsSetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields  = ["city", "timestamp"]
    search_fields = ["city", "timestamp", "weather", "weather_desc"]
    ordering_fields = [
        "timestamp",
        "city",
        "temp",
        "temp_max",
        "temp_min",
        "sunrise",
        "sunset",
    ]

    def get_queryset(self):
        cache_name = f"{self.request.user.id}_{datetime.now().day}_{datetime.now().hour}_{datetime.now().minute}"

        if cache_name in cache:
            return cache.get(cache_name)

        queryset = UserHistory.objects.filter(user__id=self.request.user.id)
        cache.set(cache_name, queryset, 60) # in 1 min

        return queryset
