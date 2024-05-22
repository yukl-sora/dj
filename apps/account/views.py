import logging
from django.shortcuts import render
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .serializers import UserRegisterSerializer, ForgotPasswordSerializer, RecoverAccountSerializer, UserVerificationSerializer
from .tasks import send_verification_code, send_recovery_code
from apps.profiles.models import UserProfile

# Create your views here.

User = get_user_model()


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request: Request) -> Response:
        try:
            serializer = UserRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            # logger.info(f"User registered successfully. User-data: {user}")
        except IntegrityError:
            # logger.error(f"User doesn't registered. User-data: {user}")
            return Response({
                "MESSAGE": "Something went wrong, please check the input",
                "STATUS": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
        
        send_verification_code.delay(user.email, user.verification_code)
        return Response(data={
            "SERIALIZER DATA": serializer.data,
            "MESSAGE": "User created successfully",
            "STATUS": status.HTTP_201_CREATED
        }, status=status.HTTP_201_CREATED)
    

class VerifyAccountAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request: Request, verification_code: str) -> Response:
        try:
            user = User.objects.get(verification_code=verification_code)
            user.is_active = True
            user.verification_code = ""
            user.save()
            serializer = UserVerificationSerializer(data=request.data)
            profile = serializer.create_profile(owner=user, data=request.data)
            return Response(data={
                "MESSAGE": "Account activated successfully!",
                "STATUS": status.HTTP_200_OK,
                "DATA": {"profile_id": profile.id, "username": profile.username}
            }, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response(data={
                "MESSAGE": "User with given email doesn't exist or already activated",
                "STATUS": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
            

class ForgotAccountAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request: Request) -> Response:
        try:
            serializer = ForgotPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            recovery = serializer.save()
            user = User.objects.get(email=request.data.get("email"))
        except User.DoesNotExist:
            return Response(data={
                "MESSAGE": "User with given email does not exist!",
                "STATUS": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
        
        send_recovery_code.delay(user.email, user.verification_code, recovery.secret)
        return Response(data={
            "id": user.id, 
            "email": user.email, 
            "verify_code": user.verification_code
        }, status=status.HTTP_200_OK)
    

class RecoveryAccountAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request: Request, verification_code: str) -> Response:
        try:
            user = User.objects.get(verification_code=verification_code)
            user.verification_code = ""
            serializer = RecoverAccountSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.set_new_password()
        except User.DoesNotExist:
            return Response(data={
                "MESSAGE": "User with given email does not exist!",
                "STATUS": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data={
            "MESSAGE": "Account recovered successfully",
        }, status=status.HTTP_200_OK)


# TODO: change password, resend verification link