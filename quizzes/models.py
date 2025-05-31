from django.db import models
from django.conf import settings
from courses.models import Lesson

class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pass_percentage = models.PositiveIntegerField(default=70)  # Percentage needed to pass
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Quiz: {self.title}"
    
    def get_questions_count(self):
        return self.questions.count()

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Question {self.order}: {self.text[:50]}..."

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.text} - {'Correct' if self.is_correct else 'Incorrect'}"

class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    max_score = models.PositiveIntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    passed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'quiz', 'completed_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}/{self.max_score} ({self.percentage}%)"
