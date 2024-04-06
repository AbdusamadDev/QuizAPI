from rest_framework.generics import CreateAPIView, RetrieveAPIView

from .models import Exam

from .serializers import ExamSerializer

class ExampView(CreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

    def get_serializer_context(self):
        return {'uuid': self.kwargs.get('uuid')} 
    
    
class ExampDetailAPIView(RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    lookup_field = 'uuid'
