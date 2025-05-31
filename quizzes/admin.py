from django.contrib import admin
from .models import Quiz, Question, Answer, QuizAttempt

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'order')
    list_filter = ('quiz',)
    inlines = [AnswerInline]

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'pass_percentage')
    list_filter = ('lesson__module__course',)
    search_fields = ('title', 'description')

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'max_score', 'percentage', 'passed', 'completed_at')
    list_filter = ('passed', 'quiz', 'user')
    search_fields = ('user__username', 'quiz__title')
