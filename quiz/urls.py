from django.urls import path
from .views import generate_quiz_view, quiz_detail_view

urlpatterns = [
    path('generate/', generate_quiz_view, name='generate_quiz'),
    path('<int:quiz_id>/', quiz_detail_view, name='quiz_detail'),
]
