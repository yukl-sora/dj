from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins

from .models import CoursesModel, CourseItemModel, CategoryModel
from .serializers import AllCoursesSerialier, CategorySerializer, CourseSerializer, CourseItemSerializer
from .permissions import IsCourseOwner
from apps.profiles.models import UserProfile

# Create your views here.
        

class AllCourseAPIView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = AllCoursesSerialier
    queryset = CoursesModel.objects.all()


class LatestCourseAPIView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = AllCoursesSerialier
    queryset = CoursesModel.objects.order_by("-created_at")[:4]

    
class CourseViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    permission_classes = [IsCourseOwner]
    serializer_class = CourseSerializer
    queryset = CoursesModel.objects.all()
    
    
class CourseItemViewSet(ModelViewSet):
    permission_classes = [IsCourseOwner]
    serializer_class = CourseItemSerializer
    queryset = CourseItemModel.objects.all()