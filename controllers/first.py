def faq(request):
    return 'faq!'

def downloads(request):
    return 'downloads'

def other(request):
    return request['REQUEST_URI']
