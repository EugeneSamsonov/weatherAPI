from rest_framework import serializers

from history.models import UserHistory


class UserHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHistory
        fields = "__all__"