from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.CharField(max_length=255, blank=True, null=True)  # Path to course image
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_total_modules(self):
        return self.modules.count()

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def get_next_module(self):
        next_modules = Module.objects.filter(
            course=self.course, 
            order__gt=self.order
        ).order_by('order')
        return next_modules.first() if next_modules.exists() else None
    
    def get_prev_module(self):
        prev_modules = Module.objects.filter(
            course=self.course, 
            order__lt=self.order
        ).order_by('-order')
        return prev_modules.first() if prev_modules.exists() else None

class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.module.title} - {self.title}"

class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'lesson']
    
    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} - {'Completed' if self.completed else 'In Progress'}"
