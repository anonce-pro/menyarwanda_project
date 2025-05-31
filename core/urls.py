from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('culture/', views.culture_view, name='culture'),
    path('geography/', views.geography_view, name='geography'),
    path('history/', views.history_view, name='history'),
]
