from typing import Dict
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from rest_framework import status

from .models import UserProfile

# Create your tests here.

User = get_user_model()


class ProfileTest(APITestCase):
    base_url = "http://localhost:8000/api/v1/profiles/"
    file_path = "./media/test/test.jpg"
    
    @property
    def example_bearer_token(self) -> Dict[str, str]:
        user = User.objects.create_user(
            email = "dosvukud@rakjake.gy",
            password = "qwerty",
            is_active = True
            )
        profile = UserProfile.objects.create(owner=user)
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}
    
    def create_random_profile(self) -> User:
        user = User.objects.create_user(
            id = 99,
            email = "ilwaguh@wieve.pa",
            password = "qwerty",
            is_active = True
            )
        profile = UserProfile.objects.create(owner=user)
        return profile
    
    def get_upload_photo(self) -> SimpleUploadedFile:
        with open(file=self.file_path, mode="rb") as file:
            return SimpleUploadedFile(
                name="test.jpg",
                content=file.read(),
                content_type="image/jpg"
            )
    
    def test_view_profile(self) -> None:
        url = self.base_url + "me/"
        response = self.client.get(path=url, **self.example_bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_detail_profile(self) -> None:
        profile = self.create_random_profile()
        url = self.base_url + f"{profile.id}/"
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_profile(self) -> None:
        url = self.base_url + "me/update/"
        photo = self.get_upload_photo()
        response = self.client.patch(path=url, data={
            "username": "Aiden",
            "photo": photo,
            "description": "especially solid soldier mistake fifteen east",
            "contacts": "+996 700 999 666",
            "youtube_url": "https://youtube.com/boskowli"
        }, format="multipart", **self.example_bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)