from os import curdir
from os.path import join as pjoin
import requests
import json
from pybufrkit.decoder import Decoder
from pybufrkit.renderer import NestedJsonRenderer
from http.server import BaseHTTPRequestHandler, HTTPServer


class StoreHandler(BaseHTTPRequestHandler):
    store_path = pjoin(curdir, 'store_test.json')
    imported_data = pjoin(curdir, 'imported.dat')

    def do_GET(self):
        if self.path == '/store.json':
            with open(self.store_path) as fh:
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                self.wfile.write(fh.read().encode())

    def json_generator(self, data):
        decoder = Decoder()
        bufr_message = decoder.process(data)
        json_data = NestedJsonRenderer().render(bufr_message)
        json_data[0][0]['value'] = 'BUFR'
        json_data[-1][0]['value'] = '7777'
        json_string = json.dumps(json_data)
        return json_string

    def do_POST(self):
        if self.path == '/imported.dat':
            length = self.headers['content-length']
            data = self.rfile.read(int(length))

            data = self.json_generator(data)

            with open(self.store_path, 'w') as fh:
                fh.write(data)
            self.send_response(200)


server = HTTPServer(('', 9998), StoreHandler)
server.serve_forever()