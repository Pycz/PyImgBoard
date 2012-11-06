from lib.url import Url
from controllers import first

#all available pages on site here
url_patterns = [Url(r'^/$', first.index),
                Url(r'^/([a-z]{1,3})/$', first.board),
                Url(r'^/faq$', first.faq),
                Url(r'^/downloads$', first.downloads),
                Url(r'^/.*$', first.other),]
