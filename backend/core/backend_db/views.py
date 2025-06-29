from django.shortcuts import render
from .models import Course, Assignment
from rest_framework import viewsets
from .models import Classroom, Enrollment, Submission, Topic, User
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UserSerializer, ClassroomSerializer, EnrollmentSerializer, CourseSerializer, AssignmentSerializer, SubmissionSerializer

from django.contrib.auth import get_user_model
User = get_user_model()

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'school/course_list.html', {'courses': courses})

def assignment_detail(request, pk):
    assignment = Assignment.objects.get(pk=pk)
    return render(request, 'school/assignment_detail.html', {'assignment': assignment})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        role = self.request.data.get('role')
        if role == User.Role.ADMIN and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only staff can create admin users.")
        serializer.save()

class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = []

    @action(detail=False, methods=['get'], url_path='my')
    def my_classes(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=400)
        classrooms = Classroom.objects.filter(enrollments__student__id=user_id)
        serializer = self.get_serializer(classrooms, many=True)
        return Response(serializer.data)



class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

