from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.exceptions import APIException
from .models import Exam, Result

from .serializers import ExamSerializer, CheckExamSerializer

from quiz.models import Question


class ExampView(CreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

    def get_serializer_context(self):
        return {"uuid": self.kwargs.get("uuid")}


class ExampDetailAPIView(RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    lookup_field = "uuid"


class CheckExamView(CreateAPIView):
    queryset = Result.objects.all()
    serializer_class = CheckExamSerializer

    def create(self, request, *args, **kwargs):
        answers = request.data.get("answers", None)
        if not answers:
            raise APIException({"data": "Data error"})
        cranswer = 0
        for ans in answers:
            try:
                qid = ans["qid"]
                anstr = ans["ans"]
                q = Question.objects.get(id=qid)
                if q.answer == anstr:
                    cranswer += 1
            except Exception as error:
                raise APIException({"detail": str(error)})
        count_q = len(answers)

        request.data["score"] = (100 / count_q) * cranswer
        return super().create(request, *args, **kwargs)

    def get_serializer_context(self):
        return {"uuid": self.kwargs.get("uuid")}
