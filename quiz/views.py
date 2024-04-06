from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Quiz, Question
from . import serializers


class AddQuizAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = serializers.QuizSerializer


class QuizzesAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = serializers.QuizSerializer

