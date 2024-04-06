from django.urls import path
from .views import ExampView, ExampDetailAPIView

urlpatterns = [
    path('detail/<uuid:uuid>/', ExampDetailAPIView.as_view(), name = 'exam_detail'),
    path('<uuid:uuid>/', ExampView.as_view(), name = 'exam_create'),
]