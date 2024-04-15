from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import APIException
from rest_framework.generics import UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView

from .serializers import TeacherSerializer, PasswordResetSerializer
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

        if (
            len(
                Teacher.objects.filter(
                    phonenumber=serializer.initial_data["phonenumber"]
                )
            )
            > 0
        ):
            raise APIException({"error": "unique"})

        serializer.is_valid(raise_exception=True)

        # except IntegrityError as e:
        #     print(111111, e)
        #     if 'unique constraint' in str(e).lower():
        #         raise APIException({"error": "unique",  status : status.HTTP_403_FORBIDDEN})

        teacher = serializer.save()

        # O'qituvchi uchun token generatsiya
        refresh = RefreshToken.for_user(teacher)
        token_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        # Success response & JWT Token
        return Response(token_data, status=status.HTTP_201_CREATED)


class RetrieveTeacherDetailsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        teacher = get_object_or_404(Teacher, pk=request.user.id)
        return Response(
            {
                "data": {
                    "id": teacher.pk,
                    "fullname": teacher.fullname,
                    "phonenumber": teacher.phonenumber,
                }
            },
            status=status.HTTP_200_OK,
        )


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


class EditProfileAPIView(UpdateAPIView):
    serializer_class = TeacherSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        user_pk = self.request.user.pk

        try:
            obj = Teacher.objects.get(id=user_pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Teacher.DoesNotExist:
            return Response(
                {"detail": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method 'PUT' not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


class ResetPasswordAPIVIew(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    queryset = Teacher.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data.get("old_password")
        new_password = serializer.validated_data.get("new_password")
        teacher = get_object_or_404(klass=Teacher, pk=request.user.pk)
        hashed_password = teacher.password

        # Checking old password
        if check_password(encoded=hashed_password, password=old_password):
            new_password = make_password(new_password)
        else:
            return Response(
                {"error": "Incorrect password provided!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        teacher.password = new_password
        teacher.save()

        return Response(
            {"data": "Password reset successfully!"}, status=status.HTTP_200_OK
        )
