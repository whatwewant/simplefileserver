#!/usr/bin/env python
# coding=utf-8

import os
import mimetypes

def server(port=8080):

    import bottle
    from bottle import route, run
    from bottle import template
    from bottle import request, response
    from bottle import error

    # import paste # multi-threaded server library -- paste, cherrypy
    # single thread: built-in wsgiref WSGIServer

    BASE_DIR = os.path.dirname(__file__)
    bottle.TEMPLATE_PATH.insert(0, BASE_DIR)
    bottle.default_app().autojson = False

    @route('/hello')
    def hello():
        return "Hello World!"

    @error(404)
    def error404(error):
        return '404: Nothing here, sorry'

    @error(500)
    def error500(error):
        return '500: Nothing here, sorry'

    @route('/')
    def index():
        # print dir(request)
        files_and_dirs = os.listdir('.')
        
        return template('templates/index.html', 
                        {'title': 'Index',
                         'request_path': '.', 
                        'files_and_dirs': files_and_dirs})

    #@route('/(?P<file_dirs>\w+)')
    # @route('/:file_dirs')
    # @route('/<path:path>')
    # def file_dir(path):
    #    return "Hello %s!" % path
    @route('/<file_dirs_path:path>')
    def file_dir(file_dirs_path):
        request_path = file_dirs_path
        server_path = file_dirs_path.replace('..', '')
        filename= os.path.join('.', file_dirs_path)
        if os.path.isfile(filename):
            start = request.headers.get('Range', 'bytes=0-')
            # print start
            try:
                pos = int(start[6:-1])
            except ValueError:
                return '400 Bad Range Specified'

            f = open(filename, 'rb')
            fs = os.fstat(f.fileno())
            
            full = fs.st_size
            if full < pos:
                f.close()
                return '400 Bad Range Out'

            start = start.replace('=', ' ')
            filetype = mimetypes.guess_type(filename)[0]

            response.add_header('Content-Length', str(full))
            response.add_header('Content-Range', '%s%s/%s' % (start, full-1, full))
            response.add_header('Accept-Ranges', 'bytes')
            response.add_header('Content-Type', filetype)
                                    #'application/octet-stream')
            f.seek(pos)
            return f

        elif os.path.isdir(filename):
            files_and_dirs = os.listdir(server_path)
            return template('templates/index.html', 
                        {'title': 'Index of' + request_path,
                         'request_path': request_path, 
                         'files_and_dirs': files_and_dirs})
        else:
            return 'Nothing'

    # single thread
    # run(port=8080, debug=True)

    # multiple threads
    run(host='0.0.0.0', server='paste', port=port, debug=True)
