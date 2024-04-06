from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import TeacherRegistrationAPIView, test


urlpatterns = [
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # bu access tokenni yangliash uchun endpoint. Access Token nisbatan tezroq expire boladi
    path(
        "token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # bu birinchi marta avtorizatsiya qilganda beriladigan access & refresh token
    path("register/", TeacherRegistrationAPIView.as_view()),
    path("test/", test),
    # path(
    #     "teachers/<int:pk>/",
    #     TeacherAuthViewSet.as_view(
    #         {
    #             "get": "details",
    #             "put": "update",
    #             "patch": "partial_update",
    #             "delete": "destroy",
    #         }
    #     ),
    # ),
]
