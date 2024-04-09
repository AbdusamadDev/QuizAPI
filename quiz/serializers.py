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
        print(self.user_id)
        
        if not Teacher.objects.filter(id=self.user_id).exists():
            redata.pop('answer')
        return redata
    

class QuizSerializer(ModelSerializer):

    class Meta:
        model = Quiz
        fields = '__all__'

    def get_questions(self, obj):
        decoded_token = unhash_token(self.context.get('request').headers)
        result = QuestionSerializer(instance=obj.question_set.all(), many=True, user_id=decoded_token['user_id'])
        return result.data

    def to_representation(self, instance):
        redata = super().to_representation(instance)
        redata['begin_date'] = instance.formatted_begin_date
        redata['end_date'] = instance.formatted_begin_date
        redata['questions'] = self.get_questions(instance)
        return redata
