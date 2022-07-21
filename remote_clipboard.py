#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""View and change clipboard remotely
"""

import os
import sys
from wsgiref.simple_server import make_server
try:
    # Python 3.8 and later 
    from html import escape
except ImportError:
    # py2
    from cgi import escape

try:
    # Python 3.8 and later 
    from urllib.parse import parse_qs
except ImportError:
    # py2
    from cgi import parse_qs


try:
    import android
    droid = android.Android()
except ImportError:
    android = droid = None

if android is None:
    try:
        import xerox  # NOTE use https://github.com/clach04/xerox/tree/win_no_crash until PR merged -- from https://github.com/kennethreitz/xerox
    except ImportError:
        if os.environ.get('FAKE_XEROX') is None:
            raise
        else:
            # no clipboard access, so store/cache locally
            class FakeXerox:
                def __init__(self):
                    self.txt = ''
                def copy(self, new_text):
                    self.txt = new_text
                def paste(self):
                    return self.txt
            xerox = FakeXerox()

def copy(new_text):
    if droid:
        droid.setClipboard(new_text)
    else:
        xerox.copy(new_text)

def paste():
    if droid:
        x = droid.getClipboard()
        result = x.result
    else:
        result = xerox.paste()
    return result

def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html')]
    # content length?

    path_info = environ['PATH_INFO']

    # Returns a dictionary in which the values are lists
    get_dict = parse_qs(environ['QUERY_STRING'])

    # POST values
    # the environment variable CONTENT_LENGTH may be empty or missing
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    # Read POST body
    request_body = environ['wsgi.input'].read(request_body_size)
    """
    print('DEBUG request_body_size', repr(request_body_size))
    if request_body_size:
        print('read with size')
        request_body = environ['wsgi.input'].read(request_body_size)
    else:
        print('read with NO size')
        request_body = environ['wsgi.input'].read()  # seen under Linux, if zero passed in, will read zero bytes!
    """
    print('DEBUG request_body', repr(request_body))
    sys.stdout.flush()  # DEBUG
    d = parse_qs(request_body.decode('utf-8'))
    print('DEBUG d', repr(d))
    new_clipboard_text = d.get('newtext')
    print('DEBUG new_clipboard_text', repr(new_clipboard_text))
    if new_clipboard_text is not None:
        new_clipboard_text = ''.join(new_clipboard_text)
        new_clipboard_text = new_clipboard_text
        copy(new_clipboard_text)
    print('DEBUG new_clipboard_text', repr(new_clipboard_text))
    ###################################################

    clipboard_contents = paste()
    result = []
    result.append('<html>')
    result.append('<head>')
    result.append('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">')
    result.append('</head>')
    print('DEBUG clipboard contents=',repr(clipboard_contents))
    x = escape(clipboard_contents)
    '''
    result.append("""
    <pre>
        <code>""")
    result.append(x)
    result.append("""</code>
    </pre>
    """)
    '''

    result.append("""
    <form accept-charset="utf-8" action="setclipboard" method="POST" id="myform" name="myform">
        <label>Current clipboard contents:</label>
        <br />
        <!-- TODO There is way to get textarea to be 100 percent via CSS and/or javascript, however most browsers allow manual resizing of text area. See http://stackoverflow.com/questions/271067/how-can-i-make-a-textarea-100-width-without-overflowing-when-padding-is-present (using a textwrapper div) -->
        <textarea rows="25" cols="80" name="newtext"  accept-charset="utf-8">""")
    result.append(x)
    result.append("""</textarea>
        <br />
        <input type="submit" value="Update clipboard"/>
    </form>
    """)
    result.append('</html>')
    #import pdb ; pdb.set_trace()
    start_response(status, response_headers)
    return [''.join(result).encode('utf-8')]


def doit():
    hostname = '0.0.0.0'
    #hostname = 'localhost'
    port = int(os.environ.get('PORT', 8000))
    print('Open http://%s:%d' % (hostname, port))
    print('Issue CTRL-C (Windows CTRL-Break instead) to stop')
    httpd = make_server(hostname, port, application)
    httpd.serve_forever()


def main(argv=None):
    if argv is None:
        argv = sys.argv

    print('Python %s on %s' % (sys.version, sys.platform))
    doit()

    return 0


if __name__ == "__main__":
    sys.exit(main())
