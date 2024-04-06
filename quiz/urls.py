from django.urls import path
from . import views


urlpatterns = [
    path('add/', views.AddQuizAPIView.as_view()),
    path('quizzes_list/', views.QuizAPIView.as_view()),
    path('edit/', views.QuizAPIView.as_view()),
]
