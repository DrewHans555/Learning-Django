""" polls/views.py """

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question


class IndexView(generic.ListView):
    """ ex: domain.com/polls/ """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions"""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """ ex: domain.com/polls/5/ """
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    """ ex: domain.com/polls/5/results/ """
    model = Question
    template_name = 'polls/results.html'


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
