class HttpHeaders:    
    CONTENT_TYPE = 'Content-Type'
    CONTENT_LENGTH = 'Content-Length'

class HttpStatusCode:
    #TODO fill definitions
    _status_code_definitions = {200: 'OK', 
                                404: 'Not Found'}
    def __init__(self, code):
        self._code = code
        self._status = HttpStatusCode._status_code_definitions[code]
    def __str__(self):
        return str(self._code) + ' ' + self._status
