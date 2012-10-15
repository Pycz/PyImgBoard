# -*- coding: utf-8 -*-
from lib.template import Template, Context

def index(request):
    template = Template('index.html')
    a = [1, 2, 3, 4, 5]
    context = Context({'title': 'Главная страница', 
                       'welcome_text': 'Добро пожаловать!', 
                       'array': a})
    result = template.render(context)
    return result

def faq(request):
    return 'faq!'

def downloads(request):
    return 'downloads'

def other(request):
    return request['REQUEST_URI']
