from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

from .models import Exam, Result


from quiz.models import Question, Quiz
from quiz.serializers import QuestionSerializer, QuizSerializer


class ExamSerializer(ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True, required=False)
    quiz = QuizSerializer(many=False, read_only=True, required=False)
    class Meta:
        model = Exam
        fields = "__all__"

    def validate(self, attrs):
        try:
            uuid = self.context.get("uuid")
            quiz = Quiz.objects.get(uuid=uuid)
            attrs["quiz"] = quiz

        except:
            raise ValidationError({"uuid": "Wring uuid"})

        return attrs

    def create(self, validated_data):
        from datetime import datetime, timedelta
        from random import sample

        now = datetime.now()
        quiz = validated_data["quiz"]
        end = now + timedelta(minutes=quiz.solving_time)
        end_date = datetime(
            quiz.end_date.year,
            quiz.end_date.month,
            quiz.end_date.day,
            quiz.end_date.hour,
            quiz.end_date.minute,
            quiz.end_date.second,
            quiz.end_date.microsecond,
        )
        start_time = datetime(
            quiz.begin_date.year,
            quiz.begin_date.month,
            quiz.begin_date.day,
            quiz.begin_date.hour,
            quiz.begin_date.minute,
            quiz.begin_date.second,
            quiz.begin_date.microsecond,
        )
        if end > end_date:
            end = end_date
        if now > end_date or now < start_time:
            raise ValidationError({"Time":"Quiz time is over"})
        
        questions = list(Question.objects.filter(quiz=quiz))

        if len(questions) > quiz.limit_questions:
            random_questions = sample(questions, quiz.limit_questions)
        else:
            random_questions = sample(questions, len(questions))

        validated_data["questions"] = random_questions
        validated_data["end_date"] = end
        validated_data["begin_date"] = now
        return super().create(validated_data)


class CheckExamSerializer(ModelSerializer):
    exam = ExamSerializer(many = False, read_only=True, required = False)
    class Meta:
        model = Result
        fields = ["id", "uuid", "score", "created_at", "exam"]
    
    def to_representation(self, instance):
        redata = super().to_representation(instance)
        redata['exam'].pop("questions")
        return redata
  
    def validate(self, attrs):
        try:
            uuid = self.context.get("uuid")
            exam = Exam.objects.get(uuid=uuid)
        except:
            raise ValidationError({"uuid": "Wring uuid"})
        
        from datetime import datetime, timedelta
        end_date = datetime(
            exam.end_date.year,
            exam.end_date.month,
            exam.end_date.day,
            exam.end_date.hour,
            exam.end_date.minute,
            exam.end_date.second,
            exam.end_date.microsecond,
        )
        start_time = datetime(
            exam.begin_date.year,
            exam.begin_date.month,
            exam.begin_date.day,
            exam.begin_date.hour,
            exam.begin_date.minute,
            exam.begin_date.second,
            exam.begin_date.microsecond,
        )
        now = datetime.now()
        solving_time = now - start_time
        exam.solving_time = int(solving_time.seconds / 60)
        exam.save()

        if end_date <= now:
            attrs["exam"] = exam
        else:
            exam.status = True
            exam.save()
            raise ValidationError({"Time": "Exam time is over"})

        correct_answers = 0
        try:
            answers = self.initial_data['answers']
        except:
            
            attrs['score'] = 0.00
            return attrs
        
        for item in answers:
            qid = item['qid']
            ans = item['ans']
            try:
                quiz = Question.objects.get(quiz = exam.quiz, id = qid)
                if not exam.questions.filter(pk = quiz.id).exists():
                    raise
                if quiz.answer == ans:
                    correct_answers += 1
            except:
                raise ValidationError({"Data": "Some questions are not related to this exam!"})
        
        count_q = exam.quiz.limit_questions
        if count_q > 0:
            attrs['score'] = (100 / count_q) * correct_answers
        else:
            attrs['score'] = 0.00
 
        return attrs

