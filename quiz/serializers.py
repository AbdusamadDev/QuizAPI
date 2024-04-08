from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from accounts.models import Teacher
from quiz.utils import unhash_token
from .models import Quiz, Question


class QuestionSerializer(ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        redata = super().to_representation(instance)
        redata.pop('answer')
        return redata
    

class QuizSerializer(ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
