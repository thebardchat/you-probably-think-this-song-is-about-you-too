#!/usr/bin/env python3
"""Tiny tailnet streaming server for the audiobook preview.

Serves a mobile-friendly player page at / and the MP3 at /audio.mp3 with
HTTP Range support (206 partial content) so Safari on iOS streams it
without downloading the whole file.
"""
import http.server
import socketserver
import os
import re

PORT = 8080
MP3 = r"C:\Users\Hubby\OneDrive\Audiobooks\You-Probably-Think-This-Song-Is-About-You-Too_PREVIEW.mp3"

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>You Probably Think This Song Is About You Too</title>
<style>
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  body { margin:0; min-height:100vh; display:flex; flex-direction:column;
         align-items:center; justify-content:center; gap:1.5rem; padding:1.5rem;
         font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
         background:#0b0b0d; color:#e8e8ea; text-align:center; }
  h1 { font-size:1.25rem; font-weight:600; line-height:1.3; margin:0; max-width:22rem; }
  .sub { font-size:.85rem; color:#8a8a90; margin:0; }
  audio { width:min(92vw,30rem); }
  .speeds { display:flex; gap:.5rem; flex-wrap:wrap; justify-content:center; }
  .speeds button { background:#1c1c20; color:#e8e8ea; border:1px solid #2c2c32;
                   border-radius:999px; padding:.5rem .9rem; font-size:.9rem; }
  .speeds button.active { background:#2f6f4f; border-color:#2f6f4f; }
  .note { font-size:.75rem; color:#5a5a60; max-width:24rem; line-height:1.4; }
</style>
</head>
<body>
  <h1>You Probably Think This Song Is About You Too</h1>
  <p class="sub">Volume Two &middot; SAPI voice preview &middot; 4h&nbsp;16m</p>
  <audio id="a" controls preload="none" src="/audio.mp3"></audio>
  <div class="speeds" id="speeds">
    <button data-r="0.75">0.75&times;</button>
    <button data-r="1" class="active">1&times;</button>
    <button data-r="1.25">1.25&times;</button>
    <button data-r="1.5">1.5&times;</button>
    <button data-r="2">2&times;</button>
  </div>
  <p class="note">Streaming over your tailnet &mdash; nothing is downloaded.
     Tap play; you can scrub anywhere.</p>
<script>
  var a = document.getElementById('a');
  document.getElementById('speeds').addEventListener('click', function(e){
    var b = e.target.closest('button'); if(!b) return;
    a.playbackRate = parseFloat(b.dataset.r);
    [].forEach.call(this.querySelectorAll('button'), function(x){ x.classList.remove('active'); });
    b.classList.add('active');
  });
</script>
</body>
</html>"""


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            body = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path.startswith("/audio.mp3"):
            self.serve_audio()
        else:
            self.send_error(404)

    def serve_audio(self):
        try:
            size = os.path.getsize(MP3)
        except OSError:
            self.send_error(404, "audio not found")
            return
        start, end = 0, size - 1
        status = 200
        rng = self.headers.get("Range")
        if rng:
            m = re.match(r"bytes=(\d*)-(\d*)", rng)
            if m:
                if m.group(1):
                    start = int(m.group(1))
                if m.group(2):
                    end = int(m.group(2))
                end = min(end, size - 1)
                status = 206
        length = end - start + 1
        self.send_response(status)
        self.send_header("Content-Type", "audio/mpeg")
        self.send_header("Accept-Ranges", "bytes")
        if status == 206:
            self.send_header("Content-Range", "bytes %d-%d/%d" % (start, end, size))
        self.send_header("Content-Length", str(length))
        self.end_headers()
        with open(MP3, "rb") as f:
            f.seek(start)
            remaining = length
            while remaining > 0:
                chunk = f.read(min(65536, remaining))
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                    break
                remaining -= len(chunk)

    def log_message(self, *args):
        pass


class ThreadedServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    with ThreadedServer(("0.0.0.0", PORT), Handler) as httpd:
        print("Serving audiobook on 0.0.0.0:%d" % PORT, flush=True)
        httpd.serve_forever()
