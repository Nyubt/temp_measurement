from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        with open('home.html') as f:
            self.wfile.write(bytes(f.read(), 'utf-8'))

    def do_POST(self):
        # Porneste ciclul de temperatura
        # intr-un thread nou
        # Porneste frigiderul
        # Citeste temperatura pina nu ajunge la nivelul stabilit
        # Opreste frigiderul
        print('Got request')
        content_length = int(self.headers['Content-Length'])
        print(self.headers)
        params = self.rfile.read(content_length).decode('utf-8')
        for keyval in params.split('&'):
            key, val = keyval.split('=')
            print(key, val)

        self.send_response(200)
        self.end_headers()

        with open('home.html') as f:
            self.wfile.write(bytes(f.read(), 'utf-8'))


address = ('', 8080)
server = HTTPServer(address, Handler)
server.serve_forever()







