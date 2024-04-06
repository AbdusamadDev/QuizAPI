from rest_framework.serializers import ModelSerializer
from .models import Quiz, Question


class QuizSerializer(ModelSerializer):

    class Meta:
        model = Quiz
        fields = '__all__'