# avaliacao/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('api/avaliacao/', views.process_evaluation, name='process_evaluation'),
    path('api/avaliacoes/', views.get_evaluations, name='get_evaluations'),
    path('api/avaliacao/<int:pk>/', views.get_evaluation, name='get_evaluation'),
    path('', views.index, name='index'),
]