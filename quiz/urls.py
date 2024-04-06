from django.urls import path
from . import views


urlpatterns = [
    path('add/', views.AddQuizAPIView.as_view()),
    path('add_question/', views.AddQuestionAPIView.as_view()),
    path('quizzes_list/', views.QuizAPIView.as_view()),
    path('edit/<int:id>/', views.EditQuizAPIView.as_view()),
    path('delete/<int:id>/', views.DeleteQuizAPIView.as_view()),
    path('edit_question/', views.QuestionAPIView.as_view()),
    path('import_questions/', views.ImportQuestionAPIView.as_view()),
]
