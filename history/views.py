from datetime import datetime
from django.shortcuts import render
from django.core.cache import cache

from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins

from history.models import UserHistory
from history.serializers import UserHistorySerializer
# Create your views here.
class UserHistoryViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
    ):

    
    serializer_class = UserHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cache_name = f"{self.request.user.id}_{datetime.now().day}_{datetime.now().hour}_{datetime.now().minute}"

        if cache_name in cache:
            return cache.get(cache_name)
        
        data = UserHistory.objects.filter(user__id=self.request.user.id)
        cache.set(cache_name, data, 60)  # for 4 min
        return data
    
    
