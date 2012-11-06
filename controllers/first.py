# -*- coding: utf-8 -*-
from lib.template import Template, Context
from lib.http import HttpResponse, Http404

def index(request):
    template = Template('index.html')
    context = Context({'welcome_text': 'Добро пожаловать'})
    result = template.render(context)
    return HttpResponse(result)

def faq(request):
    template = Template('faq.html')
    context = Context({'s': 'gogog ogogog'})
    result = template.render(context)
    return HttpResponse(result)

def downloads(request):
    return HttpResponse('downloads')

def other(request):
    return HttpResponse(request['REQUEST_URI'])

def board(request, name):
    #TODO get 'name' board comments
    return HttpResponse('name = ' + name)
