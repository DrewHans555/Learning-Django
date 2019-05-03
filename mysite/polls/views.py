""" polls/views.py """

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Question


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
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    """ ex: domain.com/polls/5/vote/ """
    return HttpResponse("You're voting on question %s." % question_id)
