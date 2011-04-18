#!/usr/bin/env python

"""
Parse log files and put them on the web. Is that crazy or what?
"""

from pyroutes import route, application, utils
from pyroutes.http.response import Response, Redirect
from pyroutes.template import TemplateRenderer

import importer

from grapher import file_grapher

renderer = TemplateRenderer()

@route('/')
def main(request, *args):
    if 'logfile' in request.FILES:
        log_data = importer.Guess(*request.FILES['logfile']).process()
        return Response(file_grapher.file_as_filelike(log_data),
                headers=[('Content-Type', 'image/png')])
    if args:
        return Redirect('/')
    return Response(renderer.render('upload.xml', {}))

if __name__ == '__main__':
    utils.devserver(application)
