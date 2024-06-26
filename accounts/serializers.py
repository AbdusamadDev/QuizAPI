from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from .models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["phonenumber", "password", "fullname"]
        extra_kwargs = {"username": {"required": False, "allow_blank": True}}

    def validate_password(self, password):
        return make_password(password)

    def validate_phonenumber(self, phonenumber):
        if Teacher.objects.filter(phonenumber=phonenumber).exists():
            print("The data: ", phonenumber)
            raise ValidationError({"error": "unique"})
        return phonenumber

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        # Check if request method is PUT or PATCH
        if request and request.method in ["PUT", "PATCH"]:
            # Remove password field from the serialized data
            data.pop("password", None)

        return data


class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
