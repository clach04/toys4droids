#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""View and change clipboard remotely
"""

import urllib  # FIXME py2 only
import os
import socket
import sys
try:
    import webbrowser
except ImportError:
    webbrowser = None
from wsgiref.simple_server import make_server
try:
    # py2
    from cgi import escape
    from cgi import parse_qs
    from urllib import quote, quote_plus
except ImportError:
    # py3
    from html import escape
    from urllib.parse import quote, quote_plus


try:
    import android
    droid = android.Android()
except ImportError:
    android = droid = None
    import xerox  # NOTE use https://github.com/clach04/xerox/tree/win_no_crash until PR merged -- from https://github.com/kennethreitz/xerox


def gen_qrcode_url(url, image_size=547):
    """Construct QR generator google URL with max size, from:

    https://chart.googleapis.com/chart? - All infographic URLs start with this root URL, followed by one or more parameter/value pairs. The required and optional parameters are specific to each image; read your image documentation.
        chs - Size of the image in pixels, in the format <width>x<height>
        cht - Type of image: 'qr' means QR code.
        chl - The data to encode. Must be URL-encoded.

    See https://google-developers.appspot.com/chart/infographics/docs/overview
    """
    url = quote(url)
    #url = quote_plus(url)
    image_size_str = '%dx%d' % (image_size, image_size)
    result = 'https://chart.googleapis.com/chart?cht=qr&chs=%s&chl=%s' % (image_size_str, url)
    return result

# Utility function to guess the IP (as a string) where the server can be
# reached from the outside. Quite nasty problem actually.

def find_ip ():
   # we get a UDP-socket for the TEST-networks reserved by IANA.
   # It is highly unlikely, that there is special routing used
   # for these networks, hence the socket later should give us
   # the ip address of the default route.
   # We're doing multiple tests, to guard against the computer being
   # part of a test installation.

   candidates = []
   for test_ip in ["192.0.2.0", "198.51.100.0", "203.0.113.0"]:
      s = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
      s.connect ((test_ip, 80))
      ip_addr = s.getsockname ()[0]
      s.close ()
      if ip_addr in candidates:
         return ip_addr
      candidates.append (ip_addr)

   return candidates[0]


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
    start_response(status, response_headers)


    ###################################################
    # the environment variable CONTENT_LENGTH may be empty or missing
    try:
      request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
      request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)
    d = parse_qs(request_body)
    new_clipboard_text = d.get('newtext')
    print('DEBUG new_clipboard_text %s' % repr(new_clipboard_text))
    if new_clipboard_text is not None:
        new_clipboard_text = ''.join(new_clipboard_text)
        new_clipboard_text = new_clipboard_text.decode('utf-8')
        copy(new_clipboard_text)
    print('DEBUG new_clipboard_text', repr(new_clipboard_text))
    ###################################################

    clipboard_contents = paste()
    result = []
    result.append('<html>')
    result.append('<head>')
    result.append('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">')
    result.append('</head>')
    print('DEBUG',repr(clipboard_contents))
    x = escape(clipboard_contents)
    #'''
    result.append("""
    <pre>
        <code>""")
    result.append(x)
    result.append("""</code>
    </pre>
    """)
    #'''

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
    bresult = ''.join(result).encode('utf-8')
    return [bresult]


def doit():
    hostname = '0.0.0.0'
    #hostname = 'localhost'
    port = 8000
    print('Open http://%s:%d' % (hostname, port))
    print('Issue CTRL-C (Windows CTRL-Break instead) to stop')

    ip_addr = find_ip()
    url_str = "http://%s:%s/" % (ip_addr, port)
    print(url_str)
    if webbrowser:
        qrcode_url = gen_qrcode_url(url_str)
        webbrowser.open(qrcode_url)

    httpd = make_server(hostname, port, application)
    httpd.serve_forever()


def main(argv=None):
    if argv is None:
        argv = sys.argv

    doit()

    return 0


if __name__ == "__main__":
    sys.exit(main())
