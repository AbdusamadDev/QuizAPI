from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response

from .models import Quiz, Question
from . import serializers


class AddQuizAPIView(CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = serializers.QuizSerializer
    
