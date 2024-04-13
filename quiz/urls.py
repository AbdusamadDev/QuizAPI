from django.urls import path
from . import views


urlpatterns = [
    path("edit_question/<int:id>/", views.QuestionAPIView.as_view()),
    path("import/", views.ImportQuizAPIView.as_view()),
    path("export/<int:pk>/", views.ExportQuizAPIView.as_view()),
    path("detail/<uuid:uuid>/", views.QuizDetailsAPIView.as_view()),
    path("delete/question/<int:pk>/", views.DeleteQuestionAPIView.as_view()),
    path("delete/<int:id>/", views.DeleteQuizAPIView.as_view()),
    path("add_question/", views.AddQuestionAPIView.as_view()),
    # path("data/", views.QuizExportImportView.as_view()),
    path("edit/<int:id>/", views.EditQuizAPIView.as_view()),
    path("quizzes_list/", views.QuizAPIView.as_view()),
    path("add/", views.AddQuizAPIView.as_view()),
]
