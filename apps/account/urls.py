from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegisterAPIView,
    VerifyAccountAPIView,
    ForgotAccountAPIView,
    RecoveryAccountAPIView
)


urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path("verify/<uuid:verification_code>/", VerifyAccountAPIView.as_view()),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("forgot/", ForgotAccountAPIView.as_view()),
    path("recover/<uuid:verification_code>/", RecoveryAccountAPIView.as_view())
]