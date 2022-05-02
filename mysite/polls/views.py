from django.http import HttpResponse, HttpRequest,Http404
from django.template import loader
from polls.models import Question




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
    response = "You're looking for the results of %s question"
    return HttpResponse(response % question_id)

def vote(request, question_id:str):
    return HttpResponse("You're vote in %s question "%question_id)