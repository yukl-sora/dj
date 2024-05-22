from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AllCourseAPIView,
    CourseViewSet,
    CourseItemViewSet,
    LatestCourseAPIView
)


router = DefaultRouter()
router.register("item", CourseItemViewSet)
router.register("latest", LatestCourseAPIView, basename="latest")
router.register("", CourseViewSet)
router.register("", AllCourseAPIView, basename="main")

urlpatterns = [
    path("", include(router.urls)),
]