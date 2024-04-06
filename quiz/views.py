
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from quiz.utils import extract_data
from .models import Quiz, Question
from accounts.models import Teacher
from . import serializers
from jwt import decode
from django.conf import settings


class AddQuizAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = serializers.QuizSerializer

    def perform_create(self, serializer):
        jwt_token = self.request.headers.get('Authorization', '').split(' ')[1]
        decoded_token = decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token['user_id']
    
        serializer.validated_data['teacher'] = Teacher.objects.get(id=user_id)
        
        serializer.save()


class QuizAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = serializers.QuizSerializer


class EditQuizAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = serializers.QuizSerializer
    lookup_field = 'id'


class AddQuestionAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer


class QuestionAPIView(generics.ListAPIView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    lookup_field = 'id'


class ImportQuestionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        quiz_id = request.data.get('quiz_id')
        file = request.data.get('file')
        extract_data(quiz_id, file)
        return Response({"recieved": True}, status=status.HTTP_200_OK)
    
