from typing import Dict
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import UserProfile
from apps.courses.models import CoursesModel
from apps.courses.serializers import AllCoursesSerialier

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = "__all__"
        
    def to_representation(self, instance: UserProfile) -> Dict[str, str | int]:
        representation = super().to_representation(instance)
        courses_object = CoursesModel.objects.filter(owner_profile=instance.id)
        user = User.objects.get(id=instance.owner.id)
        representation["owner"] = {"id": user.id, "email": user.email}
        representation["courses"] = AllCoursesSerialier(courses_object, many=True).data
        return representation