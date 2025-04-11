import openai
import json
from django.conf import settings
from django.shortcuts import redirect
from .models import Quiz, Question, Choice
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

openai.api_key = settings.OPENAI_API_KEY

@login_required
def generate_quiz_view(request):
    prompt = """
    Génère un quiz Python pour débutant avec 3 questions. 
    Chaque question doit avoir 4 choix (dont 1 correct), 
    une explication et renvoyer le tout au format JSON suivant :

    {
      "title": "Quiz Python Débutant",
      "category": "Python",
      "questions": [
        {
          "text": "Quelle est la sortie de print(2 * 3)?",
          "explanation": "L’opérateur * multiplie les nombres.",
          "choices": [
            {"text": "5", "is_correct": false},
            {"text": "6", "is_correct": true},
            {"text": "23", "is_correct": false},
            {"text": "Erreur", "is_correct": false}
          ]
        },
        ...
      ]
    }
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    content = response['choices'][0]['message']['content']
    quiz_data = json.loads(content)

    quiz = Quiz.objects.create(
        title=quiz_data['title'],
        category=quiz_data.get('category', 'Général')
    )

    for q in quiz_data['questions']:
        question = Question.objects.create(
            quiz=quiz,
            text=q['text'],
            explanation=q.get('explanation', '')
        )

        for choice in q['choices']:
            Choice.objects.create(
                question=question,
                text=choice['text'],
                is_correct=choice['is_correct']
            )

    return redirect('quiz_detail', quiz_id=quiz.id)  # à créer

from django.shortcuts import get_object_or_404

@login_required
def quiz_detail_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('choices').all()

    context = {
        'quiz': quiz,
        'questions': questions
    }
    return render(request, 'quiz/quiz_detail.html', context)
