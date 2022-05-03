from django.http import HttpResponse, HttpRequest,Http404, HttpResponseRedirect
from django.template import loader
from polls.models import Question, Choice
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

def index(request:HttpRequest):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context= {
        "latest_question_list":latest_question_list
    }
    return HttpResponse(template.render(context, request))
    

def details(request, question_id:str):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exists!")
    # question = get_object_or_404(Question, pk=question_id) pode ser utilizado com shortcuts para desacoplar 
    # Template com View
    template = loader.get_template("polls/details.html")
    return HttpResponse(template.render({"question":question}, request))

def results(request, question_id:str):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html',{'question':question})

def vote(request, question_id:str):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/details.html",
        {"question":question, "error_message":"You didnt selected a choice",})
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

