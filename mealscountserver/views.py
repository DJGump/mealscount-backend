 # mealscountserver/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.generic.base import View
from django.db import transaction

# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

class AboutPageView(TemplateView):
    template_name = "about.html"

class CalculatePageView(TemplateView):
    template_name = "calculate.html"

class ResultsPageView(TemplateView):
    template_name = "results.html"

class ContactPageView(TemplateView):
    template_name = "contact.html"
