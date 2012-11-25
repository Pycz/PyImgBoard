# -*- coding: utf-8 -*-
from lib.template import Template, Context
from lib.http import HttpResponse, HttpRequest, Http404
from lib.utils import strip_tags, wakaba
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
    test = models.Model()
    tread = models.Tread(1, models.now_timestamp())
    testlist = test.get_all_records_from(tread)
    #testlist = [models.Record(*[x for x in item]) for item in testlist]
    context = Context({'lol': testlist})
    result = template.render(context)
    return HttpResponse(result)


def downloads(request):
    return HttpResponse('downloads')

def other(request):
    return HttpResponse(request['REQUEST_URI'])

def board(request, name):
    #TODO get 'name' board comments
    return HttpResponse('name = ' + name)

def ip(request):
    return HttpResponse(Template('ip.html').render({}))

def head(request):
    if request.method == 'GET':
        st = 'GET = ' + str(request.GET) + '<br>'
    else:
        st = 'POST = ' + str(request.POST) + '<br>'
        st += 'post: ' + strip_tags(request.POST['post']) + '<br>'
        st += 'email: ' + request.POST['email'] + '<br>'

    mes = 'gogog test dhfo'
    st += wakaba(strip_tags(request.POST['post'])) + '<br>'
    for name in request:
        st += name + ': ' + str(request[name]) + '<br>'
    return HttpResponse(st)
    
