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
        if self.context["request"].method != "PATCH":
            print(self.context["request"].method)
            if Teacher.objects.filter(phonenumber=phonenumber).exists():
                raise ValidationError({"error": "unique"})
        return phonenumber

    def validate(self, attrs):
        phonenumber = attrs.get("phonenumber", None)
        if phonenumber is not None:
            existing_teacher = Teacher.objects.filter(phonenumber=phonenumber).first()
            if existing_teacher:
                # Get the current user's phone number
                current_user_phonenumber = self.context["request"].user.phonenumber
                # Check if the phone number in the database is the same as the current user's phone number
                if existing_teacher.phonenumber == current_user_phonenumber:
                    # If it's the current user's phone number, remove it from the attributes
                    attrs.pop("phonenumber")
                else:
                    # If it's not the current user's phone number, raise a validation error
                    raise serializers.ValidationError(
                        "Phone number already exists for another user"
                    )
        return attrs

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
