from django.shortcuts import render

from rest_framework.viewsets import GenericViewSet
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

    def get_queryset(self):
        return UserHistory.objects.filter(user__id=self.request.user.id)
    
