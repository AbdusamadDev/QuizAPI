from django.contrib import admin
from .models import Quiz, Question


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'title', 'limit_questions', 'solving_time']
    list_display_links = ['teacher', 'title']


@admin.register(Question)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz', 'title']
    list_display_links = ['quiz', 'title']


