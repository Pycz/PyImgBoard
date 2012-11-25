# -*- coding: utf-8 -*-
from lib.utils import now_timestamp
from lib.template import Template, Context
from lib.http import HttpResponse, HttpRequest, Http404
from lib.utils import strip_tags, wakaba
import models 
import lib.utils


def test(request):
    template = Template('addtread.html')
    context = Context({})
    result = template.render(context)
    return HttpResponse(result)

def handle_new_tread(request):
    #lib.utils.get_board_name_from_referer(request['HTTP_REFERER'])
    model = models.Model()
    if request.POST["pname"]=='':
        request.POST["pname"]="Anonymous" 
    NewRecord = models.get_simple_record(name = request.POST["pname"], email = request.POST["pmail"],
                                          title = request.POST["ptitle"],post = request.POST["ppost"])
    MyBoard = models.get_simple_board(adr = "b")
    model.add_new_tread_to_board_by_record(NewRecord, MyBoard)
    newstr = str("b")+ ", "+str(request.POST["pname"])
    con = {"lol": newstr, "boardname": "b"}
    return HttpResponse(Template('treadcreated.html').render(Context(con)))

def index(request):
    model = models.Model()
    categ = model.get_all_categorys()
    newcateg = []
    for cat in categ:
        catboard = model.get_all_boards_from_category(cat)
        newcateg.append({cat.name: catboard})
        
    template = Template('index.html')
    con = {"categorys": categ, "categ_list": newcateg, 'welcome_text': 'Добро пожаловать. Снова.'}
    context = Context(con)
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
        '''st += 'post: ' + strip_tags(request.POST['post']) + '<br>'
        st += 'email: ' + request.POST['email'] + '<br>'
'''
    mes = 'gogog test dhfo'
    #st += wakaba(strip_tags(request.POST['post'])) + '<br>'
    for name in request:
        st += name + ': ' + str(request[name]) + '<br>'
    return HttpResponse(st)

def adminum(request):
    model = models.Model()
    if request.method == 'POST':
        try: 
            if request.POST.has_key('cname'):
                model.add_new_category(models.get_simple_category(
                                                lib.utils.get_normal_string(request.POST["cname"])))
            else:
                model.add_new_board_to_category(
                                                models.get_simple_board(
                                                                lib.utils.get_normal_string(request.POST["bname"]),
                                                                lib.utils.get_normal_string(request.POST["badr"]), 
                                                                request.POST["cat"])
                                                , model.get_category_by_id(request.POST["cat"]))
        except KeyError as e:
            return HttpResponse(str(request.POST)+str(request.POST.has_key('cname')))
        
    categ = model.get_all_categorys()
    newcateg = []
    for cat in categ:
        catboard = model.get_all_boards_from_category(cat)
        newcateg.append({cat.name: catboard})

    return HttpResponse(Template('admin.html').render(Context({
                                                         "categorys": categ, 
                                                         "categ_list": newcateg})))

          
