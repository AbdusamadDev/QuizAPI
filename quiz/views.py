
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Quiz, Question
from . import serializers


class AddQuizAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = serializers.QuizSerializer


class QuizAPIView(generics.ListAPIView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = serializers.QuizSerializer
    lookup_field = 'id'

    
