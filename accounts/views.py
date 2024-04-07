from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions
from rest_framework.response import Response

from .serializers import TeacherSerializer
from .models import Teacher


class TeacherRegistrationAPIView(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get_permissions(self):
        # Registratsiya uchun authorization shart emas
        if self.action == "create":
            return []
        # Accountga o'zgarish kiritilsa token jo'natilishi kerak
        elif self.action in ["update", "partial_update"]:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher = serializer.save()

        # O'qituvchi uchun token generatsiya
        refresh = RefreshToken.for_user(teacher)
        token_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        # Success response & JWT Token
        return Response(token_data, status=status.HTTP_201_CREATED)


class ChangeAccountStatusAPIView(UpdateAPIView):
    queryset = Teacher.objects.all()
    lookup_field = "pk"

    def partial_update(self, request, *args, **kwargs):
        # Target account objectni olish
        instance = self.get_object()

        # Requestdan status valueni validatsiya qilish va ajratib olish
        account_status = request.data.get("is_active")
        if account_status is None:
            return Response(
                {"detail": "is_active field is required in the request body."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Asosiy UPDATE operation shu yerda
        instance.is_active = account_status
        instance.save(update_fields=["is_active"])

        # Success response qaytarish: status va message
        return Response(
            {
                "data": "Account status modification succeeded!",
                "status": account_status == "True",
            },
            status=status.HTTP_200_OK,
        )
