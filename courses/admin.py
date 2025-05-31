from django.contrib import admin
from .models import Course, Module, Lesson, UserProgress

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'description')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order')
    list_filter = ('module__course', 'module')
    search_fields = ('title', 'content')

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'completed_at')
    list_filter = ('completed', 'user')
    search_fields = ('user__username', 'lesson__title')
