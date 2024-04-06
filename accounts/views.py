from rest_framework.generics import CreateAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import TeacherSerializer
from .models import Teacher


class TeacherRegistrationAPIView(CreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            teacher = serializer.save()
            teacher.set_password(request.data.get("password"))
            teacher.save()

            # Generating JWT token upon successful creation
            refresh = RefreshToken.for_user(teacher)
            token_data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response(
                {"tokens": token_data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def test(request):
    return Response({"data": "messdfsdf"})


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyNDAyNTYyLCJpYXQiOjE3MTIzOTg5NjIsImp0aSI6IjI3OTNkNzExNjQxMzQyNmZhM2RhZWQ5OWEyNzY0ZWNiIiwidXNlcl9pZCI6MX0.3zm-j8pG778ULEOi-CnvsmqkvOaMEey_s3sknPPTUbw
