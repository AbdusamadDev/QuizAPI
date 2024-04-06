from django.urls import path
from . import views


urlpatterns = [
    path('add/', views.AddQuizAPIView.as_view()),
    path('add_questions/', views.AddQuestionAPIView.as_view()),
    path('quizzes_list/', views.QuizAPIView.as_view()),
    path('edit/', views.QuizAPIView.as_view()),
    path('edit_questions/', views.QuestionAPIView.as_view()),
]
