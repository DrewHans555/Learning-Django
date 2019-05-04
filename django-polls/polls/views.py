from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Choice, Question


class IndexView(generic.ListView):
    """ ex: domain.com/polls/ """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those
        set to be published in the future).
        """
        last_five_questions = Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
        return last_five_questions


class DetailView(generic.DetailView):
    """ ex: domain.com/polls/5/ """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """ Excludes any questions that aren't published yet """
        return Question.objects.filter(pub_date__lte=timezone.now())


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
        url = reverse('polls:results', args=(question.id,))
        return HttpResponseRedirect(url)


def _redisplay_question_voting_form(request, question):
    template = 'polls/detail.html'
    context = {
        'question': question,
        'error_message': "You didn't select a choice.",
    }
    return render(request, template, context)
