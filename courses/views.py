from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Module, Lesson, UserProgress

def home_view(request):
    """View for the home page"""
    return render(request, 'core/home.html')

def culture_view(request):
    """View for the culture page"""
    return render(request, 'core/culture.html')

def geography_view(request):
    """View for the geography page"""
    return render(request, 'core/geography.html')

def history_view(request):
    """View for the history page"""
    return render(request, 'core/history.html')

def courses_list_view(request):
    """View for listing all available courses"""
    courses = Course.objects.all()
    return render(request, 'courses/courses_list.html', {'courses': courses})

def course_detail_view(request, course_id):
    """View for displaying course details and modules"""
    course = get_object_or_404(Course, id=course_id)
    modules = course.modules.all().order_by('order')
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules
    })

@login_required
def module_detail_view(request, module_id):
    """View for displaying module details and lessons"""
    module = get_object_or_404(Module, id=module_id)
    lessons = module.lessons.all().order_by('order')
    
    # Check if user is a subscriber for restricted content
    if not request.user.is_subscriber and not request.user.is_staff:
        messages.warning(request, 'You need to subscribe to access full course content.')
        return redirect('subscription_page')
    
    return render(request, 'courses/module_detail.html', {
        'module': module,
        'lessons': lessons,
        'next_module': module.get_next_module(),
        'prev_module': module.get_prev_module()
    })

@login_required
def lesson_detail_view(request, lesson_id):
    """View for displaying lesson content"""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    # Check if user is a subscriber for restricted content
    if not request.user.is_subscriber and not request.user.is_staff:
        messages.warning(request, 'You need to subscribe to access full course content.')
        return redirect('subscription_page')
    
    # Mark lesson as completed when viewed
    user_progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )
    
    if not user_progress.completed:
        user_progress.completed = True
        user_progress.save()
    
    # Get module for navigation
    module = lesson.module
    
    # Get next and previous lessons
    next_lesson = lesson.module.lessons.filter(order__gt=lesson.order).order_by('order').first()
    prev_lesson = lesson.module.lessons.filter(order__lt=lesson.order).order_by('-order').first()
    
    # Check if quiz exists for this lesson
    has_quiz = hasattr(lesson, 'quiz')
    
    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson,
        'module': module,
        'next_lesson': next_lesson,
        'prev_lesson': prev_lesson,
        'has_quiz': has_quiz
    })

@login_required
def user_progress_view(request):
    """View for displaying user's progress across all courses"""
    if not request.user.is_subscriber and not request.user.is_staff:
        messages.warning(request, 'You need to subscribe to track your progress.')
        return redirect('subscription_page')
    
    # Get all courses
    courses = Course.objects.all()
    progress_data = []
    
    for course in courses:
        # Get all lessons for this course
        lessons = Lesson.objects.filter(module__course=course)
        total_lessons = lessons.count()
        
        if total_lessons > 0:
            # Get completed lessons for this course
            completed_lessons = UserProgress.objects.filter(
                user=request.user,
                lesson__module__course=course,
                completed=True
            ).count()
            
            # Calculate percentage
            percentage = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0
            
            progress_data.append({
                'course': course,
                'completed': completed_lessons,
                'total': total_lessons,
                'percentage': round(percentage, 1)
            })
    
    return render(request, 'courses/user_progress.html', {
        'progress_data': progress_data
    })
