from .models import Course,Subject
from rest_framework import routers, serializers, viewsets


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('__all__')

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields=('__all__')