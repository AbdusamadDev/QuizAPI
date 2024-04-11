from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.exceptions import ValidationError
from .models import Exam, Result

from .serializers import ExamSerializer, CheckExamSerializer

from quiz.models import Question


class ExamView(CreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

    def get_serializer_context(self):

        try:
            return {"uuid": self.kwargs.get("uuid")}
        except:
            raise ValidationError({"UUID": "Wrong uuid"})


class ExamDetailAPIView(RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    lookup_field = "uuid"


class CheckExamView(CreateAPIView):
    queryset = Result.objects.all()
    serializer_class = CheckExamSerializer

    def get_serializer_context(self):
        return {"uuid": self.kwargs.get("uuid")}
    

class ResultDetailAPIView(RetrieveAPIView):
    queryset = Result.objects.all()
    serializer_class = CheckExamSerializer
    lookup_field = "uuid"


class ResultListAPIView(ListAPIView):
    serializer_class = CheckExamSerializer
    
    def get_queryset(self):
        uuid = self.kwargs.get("uuid")
        
        return Result.objects.filter(exam__quiz__uuid = uuid)
