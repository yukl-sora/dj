from typing import Dict
from uuid import uuid4
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from .models import RecoverySecret

# Create your tests here.

User = get_user_model()


class AccountTest(APITestCase):
    base_url = "http://localhost:8000/api/v1/user/"
    
    @property
    def example_bearer_token(self) -> Dict[str, str]:
        user = User.objects.create_user(
            email = "notojiwu@tacev.lb",
            password = "qwerty",
            is_active = True,
            )
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f"Bearer: {refresh.access_token}"}
    
    def create_user(self, state: bool = True) -> User:
        raw_password = "qwerty"
        user = User.objects.create_user(
            email = "suwabo@gimemi.ki",
            password = raw_password,
            is_active = state
            )
        user.raw_password = raw_password
        return user
    
    def test_register_account(self) -> None:
        url = self.base_url + "register/"
        response = self.client.post(path=url, data={
            "email": "user@gmail.com",
            "password": "qwerty",
            "password_confirm": "qwerty"
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
    
    def test_verify_account(self) -> None:
        user = self.create_user(False)
        url = self.base_url + f"verify/{user.verification_code}/"
        response = self.client.post(path=url, data={
            "username": "MamieGeorgie93"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        
    def test_login_account(self) -> None:
        user = self.create_user()
        url = self.base_url + "login/"
        response = self.client.post(path=url, data={
            "email": user.email,
            "password": user.raw_password,
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
    
    def test_forgot_password(self) -> None:
        user = self.create_user()
        url = self.base_url + "forgot/"
        response = self.client.post(path=url, data={
            "email": user.email
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        url = self.base_url + f"recover/{response.data["verify_code"]}/"
        recovery = RecoverySecret.objects.get(email=user.email)
        response = self.client.post(path=url, data={
            "email": user.email,
            "secret": recovery.secret,
            "new_password": "business",
            "new_password_confirm": "business"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        
        url = self.base_url + "login/"
        response = self.client.post(path=url, data={
            "email": user.email,
            "password": "business",
            # "password": user.raw_password => will return 404
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)