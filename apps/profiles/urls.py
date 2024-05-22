from django.urls import path
from .views import (
    ProfileRetrieveAPIView,
    UserProfileDetailView, 
    ProfileUpdateAPIView
)


urlpatterns = [
    path("me/", UserProfileDetailView.as_view()),
    path("me/update/", ProfileUpdateAPIView.as_view()),
    path("<pk>/", ProfileRetrieveAPIView.as_view()),
]