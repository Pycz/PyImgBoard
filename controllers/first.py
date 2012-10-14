# -*- coding: utf-8 -*-
from lib.template import Template, Context

def index(request):
    template = Template('index.html')
    context = Context({'title': 'Главная страница', 
                       'welcome_text': 'Добро пожаловать!'})
    result = template.render(context)
    return result

def faq(request):
    return 'faq!'

def downloads(request):
    return 'downloads'

def other(request):
    return request['REQUEST_URI']
