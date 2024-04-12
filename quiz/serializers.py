from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from accounts.models import Teacher
from quiz.utils import unhash_token
from .models import Quiz, Question


class QuestionSerializer(ModelSerializer):
    def __init__(self, instance=None, user_id=None, data=None, **kwargs):
        self.user_id = user_id
        super().__init__(instance, data, **kwargs)

    class Meta:
        model = Question
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not self.user_id:
            representation.pop("answer")
        return representation


class QuizSerializer(ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"

    def to_representation(self, instance):
        redata = super().to_representation(instance)
        request_user = self.context.get("request")
        if request_user and hasattr(request_user, "id"):
            user_id = request_user.id
        else:
            user_id = None
        print(instance.question_set.all())
        redata["questions"] = QuestionSerializer(
            instance=instance.question_set.all(),
            many=True,
            user_id=user_id,
            context=self.context,
        ).data

        return redata
