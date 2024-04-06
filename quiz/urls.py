from django.urls import path
from . import views


urlpatterns = [
    path('add/', views.AddQuizAPIView.as_view()),
    path('quizzes_list/', views.QuizzesAPIView.as_view()),
]
