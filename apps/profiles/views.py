from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import UserProfileSerializer
from .permissions import IsProfileOwner
from .models import UserProfile

# Create your views here.


class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    

class UserProfileDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    
    def get_object(self) -> UserProfile:
        user = self.request.user
        profile = UserProfile.objects.get(owner=user.id)
        return profile
    

class ProfileUpdateAPIView(UpdateAPIView):
    permission_classes = [IsProfileOwner]
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    
    def get_object(self) -> UserProfile:
        user = self.request.user
        profile = UserProfile.objects.get(owner=user.id)
        return profile