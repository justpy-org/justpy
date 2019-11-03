# mkdocs.org docsify.js.org
import http.server
import socketserver

PORT = 8080

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving docs http://localhost:{PORT}")
    httpd.serve_forever()