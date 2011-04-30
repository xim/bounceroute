#!/usr/bin/env python

"""
Parse log files and put them on the web. Is that crazy or what?
"""

import os, sys
if 'APACHE_PID_FILE' in os.environ:
    # Hacks run if running in apache
    sys.path.insert(0, '/home/xim/dev/bounceroute/')
    os.chdir('/home/xim/dev/bounceroute/')

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
