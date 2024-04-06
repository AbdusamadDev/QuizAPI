from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework import status

from .serializers import TeacherSerializer
from .models import Teacher


class TeacherAuthViewSet(ModelViewSet):
    serializer_class = TeacherSerializer
    model = Teacher

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            password = validated_data.pop("password", None)
            if password:
                validated_data["password"] = make_password(
                    password
                )  # Encrypt the password
            self.perform_create(serializer)
        except IntegrityError:
            return Response(
                {"error": "Teacher with this phone number or username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        headers = self.get_success_headers(serializer.data)
        response_data = {
            "data": "Teacher Creation succeeded, you may obtain an authorization token!"
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
