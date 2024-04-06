from django.urls import path
from . import views


urlpatterns = [
    path('add/', views.AddQuizAPIView.as_view()),
]
