from lib import utils
from lib.headers import HttpHeaders, HttpStatusCode

class HttpResponse:
    def __init__(self, content='', status=200, content_type='text/html'):
        self.content = content
        self._status_code = HttpStatusCode(status)
        self._headers = {}
        self._headers[HttpHeaders.CONTENT_TYPE] = content_type
        self._headers[HttpHeaders.CONTENT_LENGTH] = str(len(content))

    def __getitem__(self, header):
        return self._headers.get(header)

    def __setitem__(self, header, value):
        self._headers[header] = value

    def has_header(self, header):
        return self._headers.has_key(header)

    def get_headers(self):
        return self._headers.items()

    def get_status(self):
        return str(self._status_code)


class HttpRequest:
    def __init__(self, environ={}):
        self._headers = _get_request_headers(environ)
        self.GET = _get_get_parameters(environ)
        self.POST = _get_post_parameters(environ)
        self.method = self._headers['REQUEST_METHOD']
        self.path = self._headers['PATH_INFO']
        
    def _get_request_headers(self, environ):
        request = {}
        for key in environ:
            if key.isupper():
                request[key] = environ[key]
        return request
    
    def _get_get_parameters(self, environ):
        params = {}
        spl = environ['REQUEST_URI'].split('?')
        if len(spl) <> 2:
            return params
        params = self._get_params(spl[1])
        return params
            

    def _get_post_parameters(self, environ):
        params = {}
        try:
            length = int(environ.get('CONTENT_LENGTH', '0'))
        except ValueError:
            length = 0

        if length != 0:
            return params

        body = request['wsgi.input'].read(length)
        params = self._get_params(body)
        return params


    def _get_params(self, body):
        params = {}
        i = 0
        all_params = body.split('&')
        while i < len(all_params):
            par_split = all_params[i].split('=')            
            try:
                param_name = par_split[0]
                param_value = par_split[1]
            except KeyError:
                break
            params[param_name] = param_value
            i += 1
        return params

    def __getitem__(header):
        return self._headers[header]
        

class Http404(Exception, HttpResponse):
    def __init__(self):
        file404 = utils.get_template_file('404.html')
        text = None
        if file404:
            text = file404.read()
        else:
            text = '<h1>404 Page Not Found</h1>'
        HttpResponse.__init__(self, content=text, status=404)


