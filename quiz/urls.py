from django.urls import path
from . import views


urlpatterns = [
    path('add/', views.AddQuizAPIView.as_view()),
    path('add_question/', views.AddQuestionAPIView.as_view()),
    path('quizzes_list/', views.QuizAPIView.as_view()),
    path('edit/', views.EditQuizAPIView.as_view()),
    path('edit_question/', views.QuestionAPIView.as_view()),
    path('export_questions/', views.ExportQuestionAPIView.as_view()),
]
