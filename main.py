#
# By LordRatte
# http://lord-ratte.cu.cc
#
# Cleverbot api from https://github.com/folz/cleverbot.py
# UI from http://materializecss.com/

import json
from threading import Thread
from time import sleep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import cleverbot.cleverbot as clever

CHAT_BUFFER = []
PORT = 8134
CHAT_BUFFER_MAX = 20


def start_c():
    cb1 = clever.Cleverbot()
    cb2 = clever.Cleverbot()

    a = "Hi"
    while 1:
        CHAT_BUFFER.append(["Bot A:", a])
        if len(CHAT_BUFFER) > CHAT_BUFFER_MAX:
            del CHAT_BUFFER[0]
        b = cb1.ask(a)
        CHAT_BUFFER.append(["Bot B:", b])
        if len(CHAT_BUFFER) > CHAT_BUFFER_MAX:
            del CHAT_BUFFER[0]
        a = cb2.ask(b)
        sleep(1)


# Create custom HTTPRequestHandler class
class CleverHTTPRequestHandler(BaseHTTPRequestHandler):
    # handle GET command
    def do_GET(self):
        rootdir = os.path.dirname(os.path.realpath(__file__))  # file location
        try:
            print(self.path)
            if self.path == "/":

                # send code 200 response
                self.send_response(200)

                # send header first
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # send file content to client
                with open(rootdir + "/index.html") as f:
                    self.wfile.write(f.read().encode('utf-8'))
                return
            elif self.path == "/req":
                self.send_response(200)
                # send header first
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                self.wfile.write(json.dumps(CHAT_BUFFER, separators=(',', ':')).encode('utf-8'))

        except IOError as e:
            self.send_error(404, 'file not found')
            print(e)


def run():
    print('http server is starting...')

    # ip and port of server
    # by default http server port is 80
    server_address = ('0.0.0.0', PORT)
    httpd = HTTPServer(server_address, CleverHTTPRequestHandler)
    print('http server is running on port %i' % PORT)
    httpd.serve_forever()


if __name__ == '__main__':
    t = Thread(target=start_c)
    t.start()
    run()
