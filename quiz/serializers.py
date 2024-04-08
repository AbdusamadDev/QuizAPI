from rest_framework.serializers import ModelSerializer
from .models import Quiz, Question


class QuizSerializer(ModelSerializer):

    class Meta:
        model = Quiz
        fields = '__all__'


class QuestionSerializer(ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        redata = super().to_representation(instance)
        redata.pop('answer')
        return redata