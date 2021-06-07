from django.test import TestCase
import json
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from courses.serializers import SubjectSerializer,CourseSerializer
from courses.models import Subject,Course


class SubjectTest(APITestCase):
    def test_add(self):
        data={"slug":"hello","title":"testtitle","target":"bits"}
        response = self.client.post("/api/courses",data, follow=True)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)