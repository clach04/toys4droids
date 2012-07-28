#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Simple web server - suitable for use with Python 2.x.
Known to work on Android, Windows, Linux, Jython"""

import os
import sys

import BaseHTTPServer
import SimpleHTTPServer

try:
    import easydialogs
except ImportError:
    try:
        import EasyDialogs as easydialogs
    except ImportError:
        easydialogs = None



def run_web_server(port=8000, hostname=''):
    HandlerClass = SimpleHTTPServer.SimpleHTTPRequestHandler
    ServerClass = BaseHTTPServer.HTTPServer
    protocol = "HTTP/1.0"

    server_address = (hostname, port)
    # TODO consider disabling DNS checks
    # If DNS is bad/missing, web server performance is very slow.

    HandlerClass.protocol_version = protocol
    httpd = ServerClass(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    if sa[0] == '0.0.0.0':
        if hostname == '':
            hostname = 'localhost'  # TODO determine LAN (ip) address
    print 'Open http://%s:%d' % (hostname, sa[1])
    print 'Issue CTRL-C (Windows CTRL-Break instead) to stop'
    httpd.serve_forever()


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        serve_directory = argv[1]
    except IndexError:
        defaultLocation = None
        if os.path.exists('/mnt/sdcard'):
            defaultLocation = '/mnt/sdcard'  # Android hack :-(
        if easydialogs:
            serve_directory = easydialogs.AskFolder(message='Pick a folder to share', defaultLocation=defaultLocation)
        else:
            if defaultLocation is None:
                defaultLocation = '.'
            serve_directory = defaultLocation
    
    serve_directory = os.path.abspath(serve_directory)
    if serve_directory:
        print 'serving dir', serve_directory
        os.chdir(serve_directory)
        run_web_server()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

