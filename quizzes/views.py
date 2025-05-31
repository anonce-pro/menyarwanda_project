from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Lesson
from .models import Quiz, Question, Answer, QuizAttempt

@login_required
def quiz_detail_view(request, quiz_id):
    """View for displaying quiz details and questions"""
    quiz = Quiz.objects.get(id=quiz_id)
    
    # Check if user is a subscriber
    if not request.user.is_subscriber and not request.user.is_staff:
        messages.warning(request, 'You need to subscribe to access quizzes.')
        return redirect('subscription_page')
    
    # Check if this quiz belongs to a lesson the user has access to
    lesson = quiz.lesson
    
    questions = quiz.questions.all().order_by('order')
    
    return render(request, 'quizzes/quiz_detail.html', {
        'quiz': quiz,
        'questions': questions,
        'lesson': lesson
    })

@login_required
def quiz_submit_view(request, quiz_id):
    """View for submitting quiz answers and calculating results"""
    if request.method != 'POST':
        return redirect('quiz_detail', quiz_id=quiz_id)
    
    quiz = Quiz.objects.get(id=quiz_id)
    
    # Check if user is a subscriber
    if not request.user.is_subscriber and not request.user.is_staff:
        messages.warning(request, 'You need to subscribe to access quizzes.')
        return redirect('subscription_page')
    
    questions = quiz.questions.all()
    score = 0
    max_score = questions.count()
    
    # Process each question's answer
    for question in questions:
        selected_answer_id = request.POST.get(f'question_{question.id}')
        if selected_answer_id:
            selected_answer = Answer.objects.get(id=selected_answer_id)
            if selected_answer.is_correct:
                score += 1
    
    # Calculate percentage
    percentage = (score / max_score) * 100 if max_score > 0 else 0
    passed = percentage >= quiz.pass_percentage
    
    # Save the attempt
    attempt = QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=score,
        max_score=max_score,
        percentage=percentage,
        passed=passed
    )
    
    return render(request, 'quizzes/quiz_results.html', {
        'quiz': quiz,
        'score': score,
        'max_score': max_score,
        'percentage': percentage,
        'passed': passed,
        'pass_percentage': quiz.pass_percentage
    })

@login_required
def quiz_history_view(request):
    """View for displaying user's quiz attempt history"""
    if not request.user.is_subscriber and not request.user.is_staff:
        messages.warning(request, 'You need to subscribe to view quiz history.')
        return redirect('subscription_page')
    
    attempts = QuizAttempt.objects.filter(user=request.user).order_by('-completed_at')
    
    return render(request, 'quizzes/quiz_history.html', {
        'attempts': attempts
    })
