from django.shortcuts import render
import json
from .models import Evaluation
from plan.models import Plan
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from django.core import serializers
# Create your views here.


class Json(TemplateView):
    template_name = 'evaluation/evaluation.html'


def index(request):

    if request.method == 'GET':
        eva = Plan.objects.all()
        list =  serializers.serialize('json', eva)
        return JsonResponse(list, safe=False)


