from django.shortcuts import render
from rest_framework import status, viewsets
from .serializers import ClassSerializer
from .models import Classroom

class ClassroomModelViewSet(viewsets,ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassSerializer
    permission_classes = []
