# -*- coding: utf-8 -*-
from lib.template import Template, Context

def index(request):
    template = Template('index.html')
    context = Context({'name': 'Bob'})
    result = template.render(context)
    return result

def faq(request):
    return 'faq!'

def downloads(request):
    return 'downloads'

def other(request):
    return request['REQUEST_URI']
