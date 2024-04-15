from django.http import JsonResponse
from django.shortcuts import render
from help_center.models import Question, Answer, Category, Notification


def question_list(request):
    questions = Question.objects.filter(status="published").order_by("-id")
    
    context = {
        "questions":questions
    }
    return render(request, "help/question-list.html", context)


def question_detail(request, slug):
    question = Question.objects.get(status="published", slug=slug)
    context = {
        "question":question
    }
    return render(request, "help/question-detail.html", context)


def mark_as_answered(request):
    id = request.GET['id']
    question = Question.objects.get(id=id)
    question.answer_status = "Answered"
    question.save()
    data = {
        "message":"Marked As Answered"
    }
    return JsonResponse({"data":data})


def mark_as_not_answered(request):
    id = request.GET['id']
    question = Question.objects.get(id=id)
    question.answer_status = "Not Answered"
    question.save()
    data = {
        "message":"Marked As Not Answered"
    }
    return JsonResponse({"data":data})

def mark_noti_as_seen(request):
    id = request.GET['id']
    noti = Notification.objects.get(id=id)
    noti.seen = True
    noti.save()
    data = {
        "message":"Marked As Not Answered"
    }
    return JsonResponse({"data":data})


def answer_question(request):
    id = request.GET['id']
    answer = request.GET['answer']

    question = Question.objects.get(id=id)
    Answer.objects.create(question=question, content=answer)
    Notification.objects.create(user=question.user, answer=answer, question=question)
    
    data = {
        "message":"Answered"
    }
    return JsonResponse({"data":data})