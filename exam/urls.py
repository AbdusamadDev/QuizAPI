from django.urls import path
from .views import ExamView, ExamDetailAPIView, CheckExamView, ResultDetailAPIView, ResultListAPIView

urlpatterns = [
    path('get_results/<str:uuid>/', ResultListAPIView.as_view(), name = 'results_list'),
    path('check/<str:uuid>/', CheckExamView.as_view(), name = 'check'),
    path('detail/<str:uuid>/', ExamDetailAPIView.as_view(), name = 'exam_detail'),
    path('<str:uuid>/', ExamView.as_view(), name = 'result_create'),
    path('result/<str:uuid>/', ResultDetailAPIView.as_view(), name = 'result_detail'),
]