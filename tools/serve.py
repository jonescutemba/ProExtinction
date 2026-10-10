"""Preview site/ locally with the same clean addresses as Vercel: python tools/serve.py, then open http://localhost:8000
/en serves site/en/index.html, /en/manifesto serves site/en/manifesto.html, unknown paths get site/404.html."""
import http.server, pathlib, sys
SITE = pathlib.Path(__file__).resolve().parent.parent / 'site'

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=str(SITE), **k)
    def send_head(self):
        path = self.path.split('?', 1)[0].split('#', 1)[0].rstrip('/') or '/'
        f = SITE / path.lstrip('/')
        if path != '/' and not f.is_file():
            for c in (f / 'index.html', f.with_name(f.name + '.html')):
                if c.is_file(): self.path = '/' + str(c.relative_to(SITE)); break
            else:
                self.send_response(404); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.end_headers()
                self.wfile.write((SITE / '404.html').read_bytes()); return None
        return super().send_head()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f'http://localhost:{port}')
    http.server.ThreadingHTTPServer(('', port), Handler).serve_forever()
