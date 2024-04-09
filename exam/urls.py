from django.urls import path
from .views import ExampView, ExampDetailAPIView, CheckExamView, ResultDetailAPIView

urlpatterns = [
    path('check/<str:uuid>/', CheckExamView.as_view(), name = 'check'),
    path('detail/<str:uuid>/', ExampDetailAPIView.as_view(), name = 'exam_detail'),
    path('<str:uuid>/', ExampView.as_view(), name = 'result_create'),
    path('result/<str:uuid>/', ResultDetailAPIView.as_view(), name = 'result_detail'),
]