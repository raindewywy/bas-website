# dev server ที่ปิด cache — ใช้กับ preview เท่านั้น
# URL ที่ไม่มีอยู่ตอบด้วย 404.html (สถานะ 404) เหมือน GitHub Pages
import os, sys, functools, http.server
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()
    def send_error(self, code, message=None, explain=None):
        page = os.path.join(self.directory, "404.html")
        if code != 404 or self.command != "GET" or not os.path.isfile(page):
            return super().send_error(code, message, explain)
        with open(page, "rb") as f:
            body = f.read()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
port, root = int(sys.argv[1]), sys.argv[2]
http.server.ThreadingHTTPServer(("", port), functools.partial(H, directory=root)).serve_forever()
