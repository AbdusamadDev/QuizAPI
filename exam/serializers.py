from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import APIException

from .models import Exam


from quiz.models import Question, Quiz


class ExamSerializer(ModelSerializer):
    class Meta:
        model = Exam
        # fields = ['student_fullname', 'student_group', 'quiz']
        fields = "__all__"

    def validate(self, attrs):
        try:
            uuid = self.context.get('uuid')
            quiz = Quiz.objects.get(uuid = uuid)
            attrs['quiz'] = quiz
        
        except:
            raise APIException({"uuid": "Wring uuid"})
        
        return attrs

    def create(self, validated_data):
        # print(11111111111111111111, uuid)
        from datetime import datetime, timedelta
        from random import sample
        
        now = datetime.now()
        quiz = validated_data['quiz']
        end =  now + timedelta(minutes=quiz.solving_time)
        end_date = datetime(quiz.end_date.year, quiz.end_date.month, quiz.end_date.day, quiz.end_date.hour, quiz.end_date.minute, quiz.end_date.second, quiz.end_date.microsecond)

        if end > end_date:
            end = end_date

        questions = list(Question.objects.filter(quiz = quiz))

        random_questions = sample(questions, quiz.limit_questions)
        
        answers = '['
        for q in random_questions:
            answers += q.answer + ','
        answers+=']'

        validated_data['questions'] = random_questions
        validated_data['end_date'] = end
        validated_data['begin_date'] = now
        validated_data['answers'] = answers

        return super().create(validated_data)
    