from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RetrieveTeacherDetailsAPIView,
    TeacherRegistrationAPIView,
    ChangeAccountStatusAPIView,
    ResetPasswordAPIVIew,
    EditProfileAPIView,
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
        "teachers/",
        RetrieveTeacherDetailsAPIView.as_view(),
    ),
    path("change-status/<int:pk>/", ChangeAccountStatusAPIView.as_view()),
    # path("token/blacklist/", TokenBlacklistVisew.as_view(), name="token_blacklist"),
    path("edit-profile/", EditProfileAPIView.as_view()),
]
