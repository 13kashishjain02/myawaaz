from .models import Debate
from rest_framework import routers, serializers, viewsets


class DebateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debate
        fields = ('id','pros','cons')

