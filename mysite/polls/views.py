""" polls/views.py """

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Choice, Question


def index(request):
    """ ex: domain.com/polls/ """
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = 'polls/index.html'
    context = {'latest_question_list': latest_question_list}
    return render(request, template, context)


def detail(request, question_id):
    """ ex: domain.com/polls/5/ """
    question = get_object_or_404(Question, pk=question_id)
    template = 'polls/detail.html'
    context = {'question': question}
    return render(request, template, context)


def results(request, question_id):
    """ ex: domain.com/polls/5/results/ """
    question = get_object_or_404(Question, pk=question_id)
    template = 'polls/results.html'
    context = {'question': question}
    return render(request, template, context)


def vote(request, question_id):
    """ ex: domain.com/polls/5/vote/ """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return _redisplay_question_voting_form(request, question)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def _redisplay_question_voting_form(request, question):
    template = 'polls/detail.html'
    context = {
        'question': question,
        'error_message': "You didn't select a choice.",
    }
    return render(request, template, context)
