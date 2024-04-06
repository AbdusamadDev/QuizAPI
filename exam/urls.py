from django.urls import path
from .views import ExampView, ExampDetailAPIView, CheckExamView

urlpatterns = [
    path('check/<uuid:uuid>/', CheckExamView.as_view(), name = 'check'),
    path('detail/<uuid:uuid>/', ExampDetailAPIView.as_view(), name = 'exam_detail'),
    path('<uuid:uuid>/', ExampView.as_view(), name = 'exam_create'),
]