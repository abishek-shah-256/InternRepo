from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import socketserver


class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/fruits':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            fruits = ['apple', 'banana', 'mango']
            self.wfile.write(json.dumps(fruits).encode())
        else:
            self.send_response(404)


# httpd = HTTPServer(('localhost', 8000), APIHandler)
# httpd.serve_forever()


def run_server():
    host = 'localhost'
    port = 8000

    with socketserver.TCPServer((host, port), APIHandler) as server:
        print(f'Server running on {host}:{port}...')
        server.serve_forever()
        server.shutdown(socketserver.SHUT_RDWR)
        server.close()


if __name__ == '__main__':
    run_server()