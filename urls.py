from lib.url import Url
from controllers import first

#all available pages on site here
url_patterns = [Url(r'^/$', first.index),
                Url(r'^/([a-z]{1,3})/$', first.board),
                Url(r'^/faq$', first.faq),
                Url(r'^/newtread$', first.handle_new_tread),
                Url(r'^/downloads$', first.downloads),
                Url(r'^/b$', first.b),
                Url(r'^/ip$', first.ip),
                Url(r'^/head$', first.head),
                Url(r'^/adminum$', first.adminum),
                Url(r'^/.*$', first.other),
                ]
