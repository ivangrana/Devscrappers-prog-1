#!/usr/bin/env python
"""
Test:
curl -X POST -H "Authentication: KEY" -H "Content-Type: application/json" --data '{"foo":"bar"}' http://127.0.0.1:8888
"""

import os
import json
import base64
import hashlib
import argparse
from email import utils
from datetime import datetime
from xml.etree import ElementTree as etree

from collections import defaultdict
from http.server import BaseHTTPRequestHandler, HTTPServer

parser = argparse.ArgumentParser(description='A simple server to receive and save JSON data')
parser.add_argument('FILE', type=str, help='File to save received data')
parser.add_argument('UPLOAD_DIR', type=str, help='Directory to save uploaded files')
parser.add_argument('-p', '--port', type=int, dest='PORT', default=8888, help='Port for server')
parser.add_argument('-k', '--key', type=str, dest='KEY', default=None, help='Secret key to authenticate clients')
parser.add_argument('-o', '--key-overrides', type=str, dest='OVERRIDES', default=None, help='Key overrides for clips sent to server in the format "original1:new1;original2:new2"')
args = parser.parse_args()

def idx(obj, base, overrides):
    key = base
    for override in overrides:
        a,b = override.split(":")
        if a == base:
            key = b
    return obj.get(key) if obj.get(key) is not None else obj.get(base)

overrides = []
if args.OVERRIDES:
    overrides = args.OVERRIDES.split(";")
    overrides = [x for x in overrides if len(x.split(":")) == 2]

rss_meta = {
    'title': 'hili',
    'description': 'highlights',
}
rss_mapping = {
    'link': lambda i: idx(i, 'href', overrides),
    'title': lambda i: idx(i, 'html', overrides),
    'description': lambda i: idx(i, 'text', overrides),
    'pubDate': lambda i: utils.format_datetime(datetime.fromtimestamp(i['time']/1000))
}

def gen_rss(items):
    rss = etree.Element('rss', version='2.0')
    channel = etree.SubElement(rss, 'channel')
    for key, val in rss_meta.items():
        sub = etree.SubElement(channel, key)
        sub.text = val

    for item in items:
        item_el = etree.SubElement(channel, 'item')
        for tag, fn in rss_mapping.items():
            el = etree.SubElement(item_el, tag)
            el.text = fn(item)
        for tag in item['tags']:
            el = etree.SubElement(item_el, 'category')
            el.text = tag
    return etree.tostring(rss)

def gen_html(items):
    html = ['''
        <html>
            <head>
                <meta charset="utf8">
                <style>
                    html {
                        overflow-x: hidden;
                    }
                    article {
                        margin: 4em auto;
                        max-width: 720px;
                        line-height: 1.4;
                        padding-bottom: 4em;
                        border-bottom: 2px solid black;
                        font-family: sans-serif;
                    }
                    .highlight {
                        margin: 2em 0;
                    }
                    .note {
                        margin-top: 0.5em;
                        text-align: right;
                        font-size: 0.9em;
                    }
                    .tags {
                        color: #888;
                        margin-top: 1em;
                        font-size: 0.8em;
                    }
                    a {
                        color: blue;
                    }
                    img {
                        max-width: 100%;
                    }
                </style>
            </head>
            <body>''']

    grouped = defaultdict(list)
    for d in items:
        grouped[idx(d, 'href', overrides)].append(d)

    for href, group in sorted(grouped.items(), key=lambda g: -max([idx(d, 'time', overrides) for d in g[1]])):
        html.append('''
            <article>
                <h4><a href="{href}">{title}</a></h4>'''.format(href=href, title=group[0].get('title')))
        for d in group:
            if 'file' in d:
                html.append('''
                    <div class="highlight">
                        <img src="{src}">
                        <p>{text}</p>
                        <div class="tags"><em>{tags}</em></div>
                    </div>
                '''.format(
                    src=idx(d, 'file', overrides)['src'],
                    text=idx(d, 'text', overrides),
                    tags=', '.join(idx(d, 'tags', overrides))
                ))
            else:
                html.append('''
                    <div class="highlight">
                        {html}
                        <div class="note">{note}</div>
                        <div class="tags"><em>{tags}</em></div>
                    </div>
                '''.format(
                    html=idx(d, 'html', overrides),
                    note=idx(d, 'note', overrides),
                    tags=', '.join(idx(d, 'tags', overrides))
                ))
        html.append('</article>')

    html.append('</body></html>')
    return '\n'.join(html).encode('utf8')


class JSONRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        auth_key = self.headers.get('Authentication')
        if args.KEY and args.KEY != auth_key:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'unauthorized')
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        # Get data
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        self.end_headers()

        data = self.data_string.decode('utf8')
        data = json.loads(data)

        # If a file is included, save it and save only the filename
        if 'file' in data:
            # Assume that data is base64 encoded
            b64 = base64.b64decode(data['file']['data'])

            # Generate file name by hashing file data
            # and extension based on specified content type
            fname = hashlib.sha1(b64).hexdigest()
            ext = data['file']['type'].split('/')[-1]
            fname = '{}.{}'.format(fname, ext)
            with open(os.path.join(args.UPLOAD_DIR, fname), 'wb') as f:
                f.write(b64)

            # Remove original data,
            # save only filename
            del data['file']['data']
            data['file']['name'] = fname

        # Save data
        with open(args.FILE, 'a') as f:
            f.write(json.dumps(data) + '\n')

        # Response
        self.wfile.write(b'ok')
        return

    def do_GET(self):
        with open(args.FILE, 'r') as f:
            items = map(json.loads, f.read().splitlines())

        if self.path.startswith('/rss.xml'):
            self.send_response(200)
            self.send_header('Content-type', 'text/xml')
            self.end_headers()
            self.wfile.write(gen_rss(items))
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(gen_html(items))


if __name__ == '__main__':
    print('Running on port', args.PORT)
    server = HTTPServer(('localhost', args.PORT), JSONRequestHandler)
    server.serve_forever()
