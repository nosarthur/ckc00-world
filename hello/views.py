from django.shortcuts import render
from django.views.generic import TemplateView

from django.http import HttpResponse

# Create your views here.

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)


class AboutPageView(TemplateView):
    template_name = 'about.html'


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
