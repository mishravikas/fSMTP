import re
import json
from urlparse import urlparse, parse_qs
from wsgiref.simple_server import make_server
from wsgiref.util import request_uri
import sqlite3

def serve_home(query):
    conn = sqlite3.connect('test1.db')
    ret=conn.execute("SELECT * from MAIL ORDER BY id DESC LIMIT 1")
    final=ret.fetchall()
    return json.dumps(final[0])

def handler404(start_response):
    status = "404 NOT FOUND"
    response_body = "Not found"
    response_headers = [("Content-Type", "text/html"),
                        ("Content-Length", str(len(response_body)))]
    start_response(status, response_headers)
    return response_body

def application(environ, start_response):
    # get request path and request params
    request = urlparse(request_uri(environ))
    query_dict = parse_qs(request.query)
    print request.path

    urlpatterns = (
        ('/$', serve_home),
        )

    # dispatch request to request handler
    for pattern, request_handler in urlpatterns:
        if re.match(pattern, request.path, re.I):
            response_body = request_handler(query_dict)
            break
    else:
        # error handling
        return handler404(start_response)

    status = "200 OK"
    response_headers = [("Content-Type", "application/json"),
                        ("Content-Length", str(len(response_body)))]
    start_response(status, response_headers)
    return response_body

if __name__ == '__main__':
    httpd = make_server("localhost", 8158, application)
    httpd.serve_forever()
    