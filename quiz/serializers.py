from rest_framework.serializers import ModelSerializer, SerializerMethodField
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

    def to_representation(self, instance):
        redata = super().to_representation(instance)
        redata['begin_date'] = instance.formatted_begin_date
        redata['end_date'] = instance.formatted_begin_date
        redata['questions'] = QuestionSerializer(instance=instance.question_set.all(), many=True).data
        return redata
