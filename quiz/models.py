from django.db import models
from uuid import uuid4

from accounts.models import Teacher


from quiz.validators import validate_answer_number

class CustomBaseMode(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Quiz(CustomBaseMode):
    uuid = models.UUIDField(unique=True, default=uuid4)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    begin_date = models.DateTimeField()
    end_date = models.DateTimeField()
    limit_questions = models.IntegerField(default=10)
    solving_time = models.IntegerField(default=60)

    def __str__(self) -> str:
        return self.title


class Question(CustomBaseMode):
    quiz = models.ForeignKey("Quiz", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200)
    answer = models.IntegerField(validators=[validate_answer_number])

    def __str__(self) -> str:
        return f"{self.quiz} -> {self.title}"
