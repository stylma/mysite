# kolejnosc zachowywania importow tak jak poniezej, dodatkowo alfabetycznie sortujemy

# importy z modolow systemow np import random

# importy z dodatkami ktore instalujemy
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datastructures import MultiValueDictKeyError

# importy zwiazane z aplikacja
from .models import Question, Choice

from django.http import HttpResponse

# request- pod ta zmienna kryje sie obiekt requestu, który zapisuje informacje z zadaniem uzytkowinika,
# czyli wtedy kiedy uzytkownik wchodzi w dany url

# 1. widok wszystkich opublikowanych pytan


def index(request):
    questions = Question.objects.all()
    title = 'Lista wszystkich pytan'
    context = {
        'questions': questions,
        'title': title,
    }

    # {} - kontekst, nazwa zwiazana z django
    # render- renderuje, uruchamia wszystkie zmienne itd. tak abysmy np. zamiast petli mileli n powtorzen czegos itd.

    return render(request, 'polls/index.html', context)

# 2. Wdiok szczegolowy danego pytania


def detail(request, question_id):

    #question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, id=question_id)
    title = f'Pytanie: {question.question_text}'

    context = {
        'question': question,
        'title': title,
    }

    return render(request, 'polls/detail.html', context)


def vote(request, question_id):

    question = get_object_or_404(Question, id=question_id)

    # jezeli jest pierwsza metoda to nie trzeba ifa
    # if request.method=='POST':

    # Pierwszy sposob, szybszy
    choice_form = request.POST.get('choice')

    # Drugi sposob dluzszy
    # sprawdzenie czy jest w inputcie name choice w (detail.html), jezeli nie to
    # przekierowuje na strone z detail zamiast do vote
    # try:
    #     # choice nazwa z name z detial.html w inputcie
    #     choice_form = request.POST['choice']
    # except MultiValueDictKeyError:
    #     return redirect('polls:detail', question_id)

    try:
        # wybieramy choice, ktore ma dane id z danego question
        selected_choice = question.choice_set.get(id=choice_form)
    except Choice.DoesNotExist:
        return redirect('polls:detail', question_id)

    selected_choice.votes += 1
    selected_choice.save()

    return redirect('polls:results', question_id)
    # jezeli jest pierwsza metoda to tego nie trzeba
    # else:
    #     return redirect('polls:detail', question_id)


def results(request, question_id):

    question = get_object_or_404(Question, id=question_id)
    title = f'Wyniki: {question.question_text}'

    context = {
        'question': question,
        'title': title,
    }

    return render(request, 'polls/results.html', context)

# 3. widok, który reaguje na zaglosowanie przez uzytkownika (usera)
# 4. widok z wynikiami dla danego pytania
