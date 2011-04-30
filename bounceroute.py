#!/usr/bin/env python

"""
Parse log files and put them on the web. Is that crazy or what?
"""

import os, sys
if 'APACHE_PID_FILE' in os.environ:
    # Hacks run if running in apache
    sys.path.insert(0, '/home/xim/dev/bounceroute/')
    os.chdir('/home/xim/dev/bounceroute/')

import mimetypes

from matplotlib.backends.backend_agg import FigureCanvasAgg

from pyroutes import route, application, utils
from pyroutes.http.response import Response, Redirect
from pyroutes.template import TemplateRenderer

from bounceitbaby import importer

from bounceitbaby.grapher import file_grapher

renderer = TemplateRenderer()

@route('/')
def main(request, *args):
    formats_supported = sorted(FigureCanvasAgg.filetypes.iteritems())
    formats = ({'label': ', '.join((file_type, type_name)),
                'label/for': 'id_' + file_type,
                'input/value': file_type,
                'input/id': 'id_' + file_type} \
            for file_type, type_name in formats_supported)
    if 'logfile' in request.FILES:
        file_format = str(request.POST['format'])
        logreader = importer.Guess(*request.FILES['logfile'])
        data = logreader.process()
        actors = logreader.get_actors()
        mime = mimetypes.guess_type('image.' + file_format)[0] \
                or 'application/octet-stream'
        return Response( file_grapher.file_as_filelike(data, actors,
            format=file_format), headers=[('Content-Type', mime)])
    if args:
        return Redirect('/')
    return Response(renderer.render('upload.xml', {'#format': formats}))

if __name__ == '__main__':
    utils.devserver(application)
