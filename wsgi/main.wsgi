#! /usr/bin/python
# -*- coding: utf-8 -*- 

#put your app folder
#module is not main
import sys
sys.path.insert(0, '/var/www/PyImgBoard/')

import urls

def application(environ, start_response):
    correct_url = None
    for url in urls.url_patterns:
    	if url.is_correct(environ['REQUEST_URI']):
            correct_url = url
            break

    output = ''
    #TODO 404 if false
    if correct_url:
        output = correct_url.call_function(environ)

    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
