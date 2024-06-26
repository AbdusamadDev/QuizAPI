from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import status

import zipfile

from quiz.models import Quiz, Question
from accounts.models import Teacher
from . import serializers
from .utils import (
    _import_from_xls,
    _export_to_pdf,
    _export_to_xls,
    unhash_token,
)


class AddQuizAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = serializers.QuizSerializer

    def perform_create(self, serializer):
        # Keep everything simple
        # user_id = self.request.user.id
        decoded_token = unhash_token(self.request.headers)
        user_id = decoded_token["user_id"]
        serializer.validated_data["teacher"] = Teacher.objects.get(id=user_id)
        serializer.save()


class QuizAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = serializers.QuizSerializer

    def get_queryset(self):
        user = self.request.user.id
        return Quiz.objects.filter(teacher=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request.user
        return context


class EditQuizAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = serializers.QuizSerializer
    lookup_field = "id"


class AddQuestionAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer


class QuestionAPIView(generics.ListAPIView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    lookup_field = "id"


class BaseExportQuizAPIView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = serializers.QuizSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        limit = request.query_params.get("questions_limit", None)
        instance = self.get_object()
        if limit is not None:
            if limit.isdigit():
                if int(limit) in range(1, instance.limit_questions):
                    serializer = self.get_serializer(instance)
                    return self.export(serializer.data, int(limit))
                else:
                    return Response(
                        {
                            "error": "The question limit is out of range!",
                            "tip": f"Provide number in range of (1, {instance.limit_questions})",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"error": "Please provide valid integer!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Please provide limit of questions!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def export(self, data, limit):
        raise NotImplementedError("Export method must be implemented in subclasses!")


class ExportPDFQuizAPIView(BaseExportQuizAPIView):
    def export(self, data, limit):
        pdf_file = _export_to_pdf(data, limit)
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="quiz_export.pdf"'
        response.write(pdf_file.getvalue())
        return response


class ExportXLSQuizAPIView(BaseExportQuizAPIView):
    def export(self, data, limit):
        xls_file = _export_to_xls(data, limit)
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="quiz_export.xls"'
        response.write(xls_file.getvalue())
        return response


class ImportQuizAPIView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = serializers.QuizSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Done
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "Please provide a file"}, status=400)

        if file.name.endswith(".xls"):
            try:
                data = _import_from_xls(file)
            except IndexError as msg:
                return Response(
                    {"error": str(msg)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except Exception:
                return Response(
                    {"error": "Invalid data structure inside the file!"},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
            quiz_id = request.data.get("quiz_id", None)
            quiz = get_object_or_404(Quiz, pk=quiz_id)
            if quiz_id is None:
                return Response(
                    {"error": "Quiz ID is not provided!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            for question in data:
                Question.objects.create(
                    title=question["title"],
                    option_1=question["options"][0],
                    option_2=question["options"][1],
                    option_3=question["options"][2],
                    option_4=question["options"][3],
                    answer=question["correct_answer"],
                    quiz=quiz,
                )
            return Response({"success": "Import successful"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid file format"}, status=status.HTTP_400_BAD_REQUEST
            )


class DeleteQuizAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = serializers.QuizSerializer
    lookup_field = "id"


class DeleteQuestionAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = serializers.QuizSerializer


class QuizDetailsAPIView(generics.RetrieveAPIView):
    lookup_field = "uuid"
    queryset = Quiz.objects.all()
    serializer_class = serializers.QuizSerializer
