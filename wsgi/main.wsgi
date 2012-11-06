#! /usr/bin/python
# -*- coding: utf-8 -*- 
import urls
from lib.http import Http404

def application(environ, start_response):
    correct_url = None
    for url in urls.url_patterns:
    	if url.is_correct(environ['PATH_INFO']):
            correct_url = url
            break

    if correct_url:
        response = correct_url.call_function(environ)
    else:
        response = Http404()

    start_response(response.get_status(), response.get_headers())

    return [response.content]
