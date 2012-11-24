# -*- coding: utf-8 -*-
from lib.template import Template, Context
from lib.http import HttpResponse, Http404
import models 
import sys

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

def b(request):
    template = Template('b.html')
    #try:
    test = models.Model()
    tread = models.Tread(1, "2012-10-12")
    testlist = test.get_all_records_from(tread)
    #testlist = [models.Record(*[x for x in item]) for item in testlist]
    context = Context({'lol': testlist})
    result = template.render(context)
    return HttpResponse(result)
    #except:
    return HttpResponse(str(sys.exc_info()[0])+str(sys.exc_info()[1])+str(sys.exc_info()[2]))

def downloads(request):
    return HttpResponse('downloads')

def other(request):
    return HttpResponse(request['REQUEST_URI'])

def board(request, name):
    #TODO get 'name' board comments
    return HttpResponse('name = ' + name)

def ip(request):
    return HttpResponse(Template('ip.html').render({}))
