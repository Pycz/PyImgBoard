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


class Http404(Exception, HttpResponse):
    def __init__(self):
        file404 = utils.get_template_file('404.html')
        text = None
        if file404:
            text = file404.read()
        else:
            text = '<h1>404 Page Not Found</h1>'
        HttpResponse.__init__(self, content=text, status=404)


