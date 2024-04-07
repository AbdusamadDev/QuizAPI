from django.contrib.auth.hashers import make_password
from rest_framework import serializers


from .models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["phonenumber", "password", "state", "fullname"]
        extra_kwargs = {"username": {"required": False, "allow_blank": True}}

    def validate_password(self, password):
        return make_password(password)

