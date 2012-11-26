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

def handle_new_record(request):
    model = models.Model()
    request.POST["pname"] = wakaba(strip_tags(request.POST["pname"]))
    request.POST["pmail"] = wakaba(strip_tags(request.POST["pmail"]))
    request.POST["ptitle"] = wakaba(strip_tags(request.POST["ptitle"]))
    request.POST["ppost"] = wakaba(strip_tags(request.POST["ppost"]))
    if request.POST["pname"]=='':
        request.POST["pname"]="Anonymous" 
    NewRecord = models.get_simple_record(name = request.POST["pname"], email = request.POST["pmail"],
                                          title = request.POST["ptitle"],post = request.POST["ppost"])
    MyBoard = models.get_simple_board(adr = request.POST["boardadr"])
    MyTread = model.get_tread_by_id(request.POST["treadid"], MyBoard)
    
    model.insert_record_into(MyTread, NewRecord, MyBoard)
    
    newstr = str(request.POST["boardadr"])+ ", in tread "+ str(request.POST["treadid"])+" "+str(request.POST["pname"])
    con = {"lol": newstr, "treadname": lib.utils.get_board_name_from_referer(request['HTTP_REFERER'])}
    return HttpResponse(Template('recordcreated.html').render(Context(con)))

def handle_new_tread(request):
    #lib.utils.get_board_name_from_referer(request['HTTP_REFERER'])
    request.POST["pname"] = wakaba(strip_tags(request.POST["pname"]))
    request.POST["pmail"] = wakaba(strip_tags(request.POST["pmail"]))
    request.POST["ptitle"] = wakaba(strip_tags(request.POST["ptitle"]))
    request.POST["ppost"] = wakaba(strip_tags(request.POST["ppost"]))
    model = models.Model()
    if request.POST["pname"]=='':
        request.POST["pname"]="Anonymous" 
    NewRecord = models.get_simple_record(name = request.POST["pname"], email = request.POST["pmail"],
                                          title = request.POST["ptitle"],post = request.POST["ppost"])
    MyBoard = models.get_simple_board(adr = lib.utils.get_board_name_from_referer(request['HTTP_REFERER']))
    model.add_new_tread_to_board_by_record(NewRecord, MyBoard)
    newstr = str(lib.utils.get_board_name_from_referer(request['HTTP_REFERER']))+ ", "+str(request.POST["pname"])
    con = {"lol": newstr, "boardname": lib.utils.get_board_name_from_referer(request['HTTP_REFERER'])}
    return HttpResponse(Template('treadcreated.html').render(Context(con)))

def index(request):
    model = models.Model()
    categ = model.get_all_categorys()
    newcateg = []
    for cat in categ:
        catboard = model.get_all_boards_from_category(cat)
        newcateg.append({cat.name: catboard})
        
    template = Template('index.html')
    con = {"categorys": categ, "categ_list": newcateg, 'welcome_text': 'Welcome back. Again.'}
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
    model = models.Model()
    board = models.get_simple_board(adr=name)
    all_treads = model.get_all_treads_by_date(board)

    treads = {}
    for tread in all_treads:
        treads[tread.id] = model.get_all_records_from(tread, board)

    template = Template('boards.html')
    context = Context({'treads': treads, 'board': board, 
                       'all_treads': all_treads})
    return HttpResponse(template.render(context))

def tread(request, board_adr, tread_id):
    model = models.Model()
    board = models.get_simple_board(adr=board_adr)
    tread = model.get_tread_by_id(tread_id, board=board)    
    posts = model.get_all_records_from(tread, board)
    template = Template('tread.html')
    context = Context({'board': board,'tread': tread, 'posts': posts})
    return HttpResponse(template.render(context))

def ip(request):
    return HttpResponse(Template('ip.html').render(Context({})))

def head(request):
    if request.method == 'GET':
        st = 'GET = ' + str(request.GET) + '<br>'
    else:
        st = 'POST = ' + str(request.POST) + '<br>'

    st += wakaba(strip_tags(request.POST['post'])) + '<br>'
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

          
