from .models import Debate,Pros,Cons
from rest_framework import routers, serializers, viewsets


class DebateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debate
        fields = ('id','pros','cons')

class ProsCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pros
        fields = ('comments',)

