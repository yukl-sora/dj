import string
import random
from typing import Dict
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import RecoverySecret
from apps.profiles.models import UserProfile


User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(
        required=True, 
        min_length=6, 
        write_only=True
        )
    
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "password_confirm",
        ]
        
    def validate(self, attrs: Dict[str, str]) -> Dict[str, str]:
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm")
        
        if password != password_confirm:
            serializers.ValidationError("Password didn't match.")
        return attrs
    
    def create(self, validated_data: Dict[str, str]) -> User:
        user = User.objects.create_user(**validated_data)
        # user.save()
        return user
    
    
class UserVerificationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, write_only=True)
    
    def create_profile(self, owner: User, data: str) -> UserProfile:
        profile = UserProfile.objects.create(owner=owner, username=data.get("username"))
        profile.save()
        return profile
        
    
class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, write_only=True)
    
    class Meta:
        model = RecoverySecret
        fields = ["email"]
    
    def validate_email(self, email: str) -> str:
        user = User.objects.get(email=email)
        user.create_verification_code()
        user.save()
        return email
    
    def create(self, validated_data: Dict[str, str]) -> RecoverySecret:
        letters = string.ascii_uppercase
        secret = "".join(random.choice(letters) for i in range(6))
        email = self.validated_data["email"]
        recovery = RecoverySecret.objects.create(email=email, secret=secret)
        return recovery
    

class RecoverAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    secret = serializers.CharField(required=True, min_length=6)
    new_password = serializers.CharField(min_length=6)
    new_password_confirm = serializers.CharField(min_length=6)
    
    def validate_secret(self, secret: str) -> str:
        if not RecoverySecret.objects.filter(secret=secret).exists():
            raise serializers.ValidationError("Given secret is not valid.")
        return secret
    
    def validate(self, attrs: Dict[str, str]) -> Dict[str, str]:
        password = attrs.get("new_password")
        password_confirm = attrs.pop("new_password_confirm")
        
        if password != password_confirm:
            serializers.ValidationError("Password didn't match.")
        return attrs
    
    def set_new_password(self) -> None:
        user = User.objects.get(email=self.validated_data["email"])
        user.password = make_password(self.validated_data["new_password"])
        RecoverySecret.objects.get(email=user.email).delete()
        user.verification_code = ""
        user.save()
        
        
# TODO: change password, resend verification link