import http.server
import socketserver
import json
import os
import urllib.parse
from backend.replay.replay_engine import VSMKReplayGraph
from backend.utils.logger import logger

PORT = 8000
WEB_ROOT = os.path.abspath("frontend")

class VSMKHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # API Routes
        if path.startswith("/api/timeline"):
            self.handle_timeline()
        elif path.startswith("/api/replay/"):
            decision_id = path.split("/")[-1]
            self.handle_replay(decision_id)
        # Static Files
        else:
            if path == "/":
                path = "/pages/index.html"
            
            # Security check to prevent directory traversal
            # (SimpleHTTPRequestHandler handles this but we are manipulating path)
            full_path = os.path.join(WEB_ROOT, path.lstrip("/"))
            
            # Map /assets, /styles, /pages to frontend directory
            # If path starts with /assets, it maps to frontend/assets
            # full_path logic above does this: frontend/assets/...
            
            if os.path.exists(full_path) and os.path.isfile(full_path):
                self.send_response(200)
                # Set content type
                if full_path.endswith(".html"):
                    self.send_header("Content-type", "text/html")
                elif full_path.endswith(".css"):
                    self.send_header("Content-type", "text/css")
                elif full_path.endswith(".js"):
                    self.send_header("Content-type", "application/javascript")
                self.end_headers()
                with open(full_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File not found")

    def handle_timeline(self):
        graph = VSMKReplayGraph()
        data = graph.get_timeline()
        self._send_json(data)

    def handle_replay(self, decision_id):
        graph = VSMKReplayGraph()
        data = graph.replay_decision(decision_id)
        self._send_json(data)

    def _send_json(self, data):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

def run_server():
    logger.info(f"Starting SOC-MIND Server on port {PORT}...")
    logger.info(f"Serving frontend from {WEB_ROOT}")
    # Change directory so SimpleHTTPRequestHandler finds files relative to frontend if needed
    # But we are handling static files manually or mapping them.
    # To use default behavior for some, we could chdir, but our manual handler is safer for structure.
    
    with socketserver.TCPServer(("", PORT), VSMKHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        logger.info("Server stopped.")
