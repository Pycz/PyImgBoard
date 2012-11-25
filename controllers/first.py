# -*- coding: utf-8 -*-
from lib.utils import now_timestamp
from lib.template import Template, Context
from lib.http import HttpResponse, HttpRequest, Http404
from lib.utils import strip_tags, wakaba
import models 
import lib.utils
import lib.model_utils


def index(request):
    template = Template('index.html')
    context = Context({'welcome_text': 'Добро пожаловать. Снова.'})
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
    tread = models.Tread(1, now_timestamp())
    testlist = test.get_all_records_from(tread)
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

def adminum(request):
    model = models.Model()
    if request.method == 'POST':
        if request.has_key("сname"):
            model.add_new_category(lib.model_utils.get_simple_category(
                                            lib.utils.get_normal_string(request["cname"])))
        else:
            model.add_new_board_to_category(
                                            lib.model_utils.get_simple_board(
                                                            lib.utils.get_normal_string(request["bname"]),
                                                            lib.utils.get_normal_string(request["badr"]), 
                                                            request["cat"])
                                            , model.get_category_by_id(request["cat"]))
    categ = model.get_all_categorys()
    boards = {}
    for cat in categ:
        boards[cat] = model.get_all_boards_from_category(cat)

    return HttpResponse(Template('admin.html').render(Context({
                                                         "categorys": categ, 
                                                         "boards_dict": boards})))

          
