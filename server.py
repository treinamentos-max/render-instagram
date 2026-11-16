#!/usr/bin/env python3
"""Servico minimo: recebe HTML, devolve um link publico para a imagem JPEG.

POST /render         {"html": "...", "width": 1080, "height": 1350}  -> {"id","url"}
POST /render-batch   {"slides": [{"html","width","height"}, ...]}    -> {"urls": [...]}
GET  /m/<id>.jpg     entrega a imagem (publico; o id e aleatorio e nao adivinhavel)
GET  /health         verificacao simples

Seguranca: POST exige o cabecalho X-Token igual a variavel TOKEN.
Limpeza: arquivos com mais de RETENTION_HOURS horas sao apagados a cada hora.
Sem dependencias externas alem de Chromium e Pillow.
"""
import json
import os
import re
import secrets
import shutil
import subprocess
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from PIL import Image

import templates

PORT = int(os.environ.get("PORT", "8080"))
DATA_DIR = os.environ.get("DATA_DIR", "/data")
TOKEN = os.environ.get("TOKEN", "")
PUBLIC_BASE_URL = os.environ.get("PUBLIC_BASE_URL", "").rstrip("/")
RETENTION_HOURS = float(os.environ.get("RETENTION_HOURS", "72"))
MAX_BODY = 40 * 1024 * 1024
MAX_DIM = 4000
EXTRA_HEIGHT = 300
JPEG_QUALITY = int(os.environ.get("JPEG_QUALITY", "92"))

ID_RE = re.compile(r"^[0-9a-f]{24}$")
RENDER_LOCK = threading.Lock()  # uma renderizacao por vez: protege a memoria da VPS


def find_chrome():
    env = os.environ.get("CHROME_BIN")
    if env:
        return env
    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
        path = shutil.which(name)
        if path:
            return path
    raise RuntimeError("Chromium nao encontrado")


CHROME = find_chrome()


def render_html(html, width, height):
    """Renderiza o HTML em um JPEG exato (width x height). Devolve o id."""
    img_id = secrets.token_hex(12)
    out_path = os.path.join(DATA_DIR, img_id + ".jpg")
    with RENDER_LOCK, tempfile.TemporaryDirectory() as tmp:
        html_path = os.path.join(tmp, "slide.html")
        png_path = os.path.join(tmp, "shot.png")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        cmd = [
            CHROME,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            "--default-background-color=FFFFFFFF",
            "--virtual-time-budget=3000",
            "--user-data-dir=" + os.path.join(tmp, "profile"),
            # Janela maior que a arte: alguns Chromium headless entregam uma area
            # menor que a pedida. Depois recortamos exatamente width x height.
            "--window-size=%d,%d" % (width, height + EXTRA_HEIGHT),
            "--screenshot=" + png_path,
            "file://" + html_path,
        ]
        proc = subprocess.run(cmd, capture_output=True, timeout=60)
        if not os.path.exists(png_path):
            raise RuntimeError("Falha ao renderizar: " + proc.stderr.decode("utf-8", "ignore")[-300:])
        img = Image.open(png_path).convert("RGB")
        if img.width < width or img.height < height:
            raise RuntimeError(
                "Captura menor que o pedido (%dx%d < %dx%d)" % (img.width, img.height, width, height)
            )
        img = img.crop((0, 0, width, height))
        img.save(out_path, "JPEG", quality=JPEG_QUALITY, optimize=True)
    return img_id


def foto_data_uri(b64):
    """Converte a foto (base64, PNG/JPEG) em JPEG leve embutido no HTML. None se invalida."""
    if not b64:
        return None
    try:
        import base64
        import io
        img = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")
        if img.width > 1400:
            img = img.resize((1400, int(img.height * 1400 / img.width)))
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=88, optimize=True)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:  # noqa: BLE001
        return None


def public_url(handler, img_id):
    base = PUBLIC_BASE_URL
    if not base:
        host = handler.headers.get("Host", "localhost")
        base = "http://" + host
    return "%s/m/%s.jpg" % (base, img_id)


def clean_old_files():
    limit = time.time() - RETENTION_HOURS * 3600
    removed = 0
    for name in os.listdir(DATA_DIR):
        if not name.endswith(".jpg"):
            continue
        path = os.path.join(DATA_DIR, name)
        try:
            if os.path.getmtime(path) < limit:
                os.remove(path)
                removed += 1
        except OSError:
            pass
    return removed


def cleaner_loop():
    while True:
        try:
            n = clean_old_files()
            if n:
                print("limpeza: %d arquivo(s) apagado(s)" % n, flush=True)
        except Exception as exc:  # noqa: BLE001
            print("erro na limpeza:", exc, flush=True)
        time.sleep(3600)


def parse_dim(value, default):
    try:
        v = int(value)
    except (TypeError, ValueError):
        return default
    return max(100, min(MAX_DIM, v))


class Handler(BaseHTTPRequestHandler):
    server_version = "render/1.0"

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args), flush=True)

    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def authorized(self):
        return bool(TOKEN) and secrets.compare_digest(self.headers.get("X-Token", ""), TOKEN)

    def read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_BODY:
            raise ValueError("corpo ausente ou grande demais")
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self):
        if self.path == "/health":
            files = len([n for n in os.listdir(DATA_DIR) if n.endswith(".jpg")])
            return self.send_json(200, {"ok": True, "arquivos": files})
        m = re.match(r"^/m/([0-9a-f]{24})\.jpg$", self.path)
        if m and ID_RE.match(m.group(1)):
            path = os.path.join(DATA_DIR, m.group(1) + ".jpg")
            if os.path.exists(path):
                with open(path, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "image/jpeg")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Cache-Control", "public, max-age=3600")
                self.end_headers()
                self.wfile.write(data)
                return
        self.send_json(404, {"erro": "nao encontrado"})

    def do_POST(self):
        if not self.authorized():
            return self.send_json(401, {"erro": "token invalido"})
        try:
            body = self.read_json()
            if self.path == "/render":
                html = body["html"]
                w = parse_dim(body.get("width"), 1080)
                h = parse_dim(body.get("height"), 1350)
                img_id = render_html(html, w, h)
                return self.send_json(200, {"id": img_id, "url": public_url(self, img_id)})
            if self.path == "/render-day":
                # Recebe o conteudo do dia (texto) e devolve os links das artes prontas.
                fotos = body.pop("fotos", None) or {}
                out = {"revisar": templates.revisar(body)}
                car = body.get("carrossel") or {}
                for nome, bloco in (("capa", car), ("imagem", body.get("imagem")), ("stories", body.get("stories"))):
                    uri = foto_data_uri(fotos.get(nome))
                    if uri and isinstance(bloco, dict):
                        bloco["foto"] = uri
                out["fotos_usadas"] = sorted(n for n in fotos if fotos.get(n))
                out["carrossel"] = [
                    public_url(self, render_html(h, w, hh)) for (h, w, hh) in templates.slides_carrossel(car)
                ]
                out["imagem"] = [
                    public_url(self, render_html(h, w, hh)) for (h, w, hh) in templates.post_imagem(body.get("imagem") or {})
                ][0]
                out["stories"] = [
                    public_url(self, render_html(h, w, hh)) for (h, w, hh) in templates.post_stories(body.get("stories") or {})
                ][0]
                return self.send_json(200, out)
            if self.path == "/render-batch":
                urls = []
                for slide in body["slides"][:12]:
                    img_id = render_html(
                        slide["html"],
                        parse_dim(slide.get("width"), 1080),
                        parse_dim(slide.get("height"), 1350),
                    )
                    urls.append(public_url(self, img_id))
                return self.send_json(200, {"urls": urls})
            return self.send_json(404, {"erro": "rota desconhecida"})
        except (KeyError, ValueError, json.JSONDecodeError) as exc:
            return self.send_json(400, {"erro": "requisicao invalida: %s" % exc})
        except Exception as exc:  # noqa: BLE001
            return self.send_json(500, {"erro": str(exc)})


def main():
    if not TOKEN:
        raise SystemExit("Defina a variavel TOKEN (senha do servico).")
    os.makedirs(DATA_DIR, exist_ok=True)
    threading.Thread(target=cleaner_loop, daemon=True).start()
    print("Servico no ar na porta %d (retencao %.0f h)" % (PORT, RETENTION_HOURS), flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
