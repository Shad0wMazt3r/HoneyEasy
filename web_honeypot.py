import http.server
import socketserver
import os
import env_loader
import logger

PORT = int(env_loader.load("HTTP_PORT"))
DIRECTORY = env_loader.load("HTTP_DIRECTORY")
LOG_FILE = env_loader.load("HTTP_LOG")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        log_data = f"GET request,\nPath: {self.path}\nHeaders:\n{self.headers}"
        logger.log(log_data + "\n", LOG_FILE)
        super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        log_data = f"POST request,\nPath: {self.path}\nHeaders:\n{self.headers}\n\nBody:\n{post_data.decode('utf-8')}"
        logger.log(log_data + "\n", LOG_FILE)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"POST request received!")

if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)

logger.log('Starting server...\n', LOG_FILE)

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving HTTP on port {PORT}")
    print(f"Open http://localhost:{PORT}/ in your browser")
    logger.log(f"Serving HTTP on port {PORT}\n", LOG_FILE)
    httpd.serve_forever()
