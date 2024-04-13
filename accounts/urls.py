from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    # TokenBlacklistView,
    TokenRefreshView,
)

from .views import (
    TeacherRegistrationAPIView,
    ChangeAccountStatusAPIView,
    EditProfileAPIView,
    ResetPasswordAPIVIew,
)


urlpatterns = [
    path("reset/", ResetPasswordAPIVIew.as_view()),
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # bu access tokenni yangliash uchun endpoint. Access Token nisbatan tezroq expire boladi
    path(
        "token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # bu birinchi marta avtorizatsiya qilganda beriladigan access & refresh token
    path(
        "register/",
        TeacherRegistrationAPIView.as_view({"post": "create", "get": "list"}),
    ),
    path(
        "teachers/<int:pk>/",
        TeacherRegistrationAPIView.as_view({"get": "retrieve"}),
    ),
    path("change-status/<int:pk>/", ChangeAccountStatusAPIView.as_view()),
    # path("token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("edit-profile/", EditProfileAPIView.as_view()),
]
