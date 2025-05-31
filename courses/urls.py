from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.courses_list_view, name='courses_list'),
    path('courses/<int:course_id>/', views.course_detail_view, name='course_detail'),
    path('modules/<int:module_id>/', views.module_detail_view, name='module_detail'),
    path('lessons/<int:lesson_id>/', views.lesson_detail_view, name='lesson_detail'),
    path('progress/', views.user_progress_view, name='user_progress'),
]
