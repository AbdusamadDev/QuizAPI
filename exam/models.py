from django.db import models

import uuid

class Exam(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    student_fullname = models.CharField(max_length=60)
    student_group = models.CharField(max_length=20)
    begin_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    solving_time = models.PositiveSmallIntegerField(default=0)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    questions = models.ManyToManyField('quiz.Question', null=True, blank=True)
    answers = models.CharField(max_length=1000, blank=True, null=True)
    
    quiz = models.ForeignKey('quiz.Quiz', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.student_fullname}"


class Result(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)