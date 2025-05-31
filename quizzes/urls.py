from django.urls import path
from . import views

urlpatterns = [
    path('quiz/<int:quiz_id>/', views.quiz_detail_view, name='quiz_detail'),
    path('quiz/<int:quiz_id>/submit/', views.quiz_submit_view, name='quiz_submit'),
    path('quiz/history/', views.quiz_history_view, name='quiz_history'),
]
