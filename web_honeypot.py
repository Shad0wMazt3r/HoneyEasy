import http.server
import socketserver
import logging
import os
import env_loader

PORT = int(env_loader.load("HTTP_PORT"))
DIRECTORY = env_loader.load("HTTP_DIRECTORY")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def do_GET(self):
        logging.info(f"GET request,\nPath: {self.path}\nHeaders:\n{self.headers}")
        super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logging.info(f"POST request,\nPath: {self.path}\nHeaders:\n{self.headers}\n\nBody:\n{post_data.decode('utf-8')}")
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"POST request received!")

if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)

logging.basicConfig(filename='http_server.log', level=logging.INFO)
logging.info('Starting server...')

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving HTTP on port {PORT}")
    print(f"Open http://localhost:{PORT}/ in your browser")
    logging.info(f"Serving HTTP on port {PORT}")
    httpd.serve_forever()
