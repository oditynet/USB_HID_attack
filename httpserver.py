#!/usr/bin/env python3
import os
import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler

UPLOAD_DIR = "/tmp/pub"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class UploadHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path.rstrip('/') != "/pub":
            self.send_error(404, "Only /pub is allowed")
            return

        content_type = self.headers.get('content-type')
        if not content_type or not content_type.startswith('multipart/form-data'):
            self.send_error(400, "Only multipart/form-data supported")
            return

        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': content_type,
                }
            )

            # Проверяем наличие поля 'file'
            if 'file' not in form:
                self.send_error(400, "Missing 'file' field in form")
                return

            file_item = form['file']

            # Проверка: это действительно файл (а не просто строка)?
            if not hasattr(file_item, 'filename') or not file_item.filename:
                self.send_error(400, "Field 'file' is not a valid file upload")
                return

            filename = os.path.basename(file_item.filename)
            if not filename:
                self.send_error(400, "Empty filename")
                return

            safe_path = os.path.join(UPLOAD_DIR, filename)

            # Защита от path traversal
            real_upload_dir = os.path.abspath(UPLOAD_DIR)
            real_safe_path = os.path.abspath(safe_path)
            if not real_safe_path.startswith(real_upload_dir):
                self.send_error(403, "Path traversal detected")
                return

            # Читаем данные
            file_data = file_item.file.read()
            with open(safe_path, 'wb') as f:
                f.write(file_data)

            print(f"[+] Saved: {safe_path} ({len(file_data)} bytes)")
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK\n")

        except Exception as e:
            print(f"[!] Error: {e}")
            self.send_error(500, str(e))

    def do_GET(self):
        self.send_error(405, "GET not allowed")

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), UploadHandler)
    print("🚀 POST-сервер запущен на порту 8000")
    print("📁 Файлы сохраняются в:", os.path.abspath(UPLOAD_DIR))
    server.serve_forever()
