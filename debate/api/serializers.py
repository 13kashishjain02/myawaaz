from debate.models import Debate,Pros,Cons
from rest_framework import routers, serializers, viewsets


class DebateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pros
        # fields = '__all__'
        exclude = ['debate_pros','comment','proslike']



