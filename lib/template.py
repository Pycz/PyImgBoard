# -*- coding: utf-8 -*-
import settings

class Template:
    def __init__(self, template_name):
        self.template_name = template_name

    def render(self, context):
        template = None
        for dir in settings.TEMPLATE_DIRS:
            try:
                template = open(dir + self.template_name)
                break
            except IOError:
                pass

        output = ''
        if not template:
            #TODO raise exception
            return output

        for line in template:
            output += line

        return output

class Context:
    def __init__(self, context):
        self.context = context
