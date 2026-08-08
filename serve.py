#!/usr/bin/env python3
"""morse-trainer 静态服务 + 反馈转发到微信（hermes 通道）。

用法:
    python3 serve.py [端口]          # 默认 8080

行为:
    GET  /*            -> 伺服当前目录静态文件（默认页 index.html）
    POST /api/feedback -> 写入 feedback.log，并通过 `hermes send` 转发到微信

环境变量:
    FEEDBACK_DRY_RUN=1   只写 feedback.log，不真正发微信（测试用）
    HERMES_TARGET        hermes send 的目标，默认 weixin（home channel）
    HERMES_BIN           hermes 可执行文件路径，默认 PATH 里的 hermes
    BIND_HOST            监听地址，默认 127.0.0.1（只接受本机连接，
                         前面有 cloudflared/nginx 反代时这就够了；
                         需要对局域网/公网直连时设为 0.0.0.0）

测试:
    FEEDBACK_DRY_RUN=1 python3 serve.py 8080 &
    curl -X POST localhost:8080/api/feedback -H 'Content-Type: application/json' \
         -d '{"msg":"测试反馈","contact":"张三"}'
    tail -1 feedback.log
    # 验证真实微信通道（不启动服务也可直接测）:
    hermes send --to weixin "morse-trainer 反馈通道测试"
"""
import json
import os
import shutil
import subprocess
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(ROOT, "feedback.log")
MAX_BODY = 8192

HERMES_BIN = os.environ.get("HERMES_BIN", "hermes")
HERMES_TARGET = os.environ.get("HERMES_TARGET", "weixin")
DRY_RUN = os.environ.get("FEEDBACK_DRY_RUN") == "1"
BIND_HOST = os.environ.get("BIND_HOST", "127.0.0.1")


def forward_to_wechat(text):
    """通过 hermes 微信通道发送。返回 (ok, detail)。"""
    if DRY_RUN:
        return True, "dry-run"
    if not shutil.which(HERMES_BIN):
        return False, "hermes 不在 PATH 中"
    try:
        p = subprocess.run(
            [HERMES_BIN, "send", "--to", HERMES_TARGET, "-q", text],
            capture_output=True, text=True, timeout=60,
        )
    except subprocess.TimeoutExpired:
        return False, "hermes send 超时"
    except OSError as e:
        return False, "hermes 调用失败: %s" % e
    if p.returncode != 0:
        return False, "hermes 退出码 %d: %s" % (p.returncode, (p.stderr or p.stdout).strip()[:200])
    return True, "sent"


class Handler(BaseHTTPRequestHandler):
    server_version = "morse-trainer/1.0"

    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))

    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path.split("?")[0] != "/api/feedback":
            self._json(404, {"ok": False, "error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_BODY:
            self._json(400, {"ok": False, "error": "bad length"})
            return
        try:
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            self._json(400, {"ok": False, "error": "bad json"})
            return
        msg = str(data.get("msg", "")).strip()[:2000]
        if not msg:
            self._json(400, {"ok": False, "error": "empty msg"})
            return
        contact = str(data.get("contact", "")).strip()[:100]
        page = str(data.get("page", "")).strip()[:300]
        ua = str(data.get("ua", "")).strip()[:200]
        ip = self.client_address[0]
        ts = time.strftime("%Y-%m-%d %H:%M:%S")

        record = {"ts": ts, "ip": ip, "contact": contact, "msg": msg, "page": page, "ua": ua}
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        # 含访客 IP/联系方式，收紧权限（仅属主可读写）
        try:
            os.chmod(LOG, 0o600)
        except OSError:
            pass

        text = "📡 morse-trainer 反馈\n%s\n—— %s\n(%s, %s)" % (
            msg, contact or "匿名", ts, ip)
        ok, detail = forward_to_wechat(text)
        if ok:
            self._json(200, {"ok": True})
        else:
            # 已落盘，微信转发失败也返回 200，避免用户重复提交；detail 记日志
            sys.stderr.write("[feedback] wechat forward failed: %s\n" % detail)
            self._json(200, {"ok": True, "forwarded": False})

    def do_GET(self):
        if self.path.split("?")[0] == "/api/health":
            self._json(200, {"ok": True, "dry_run": DRY_RUN})
            return
        # 静态文件
        path = self.path.split("?")[0].split("#")[0]
        if path == "/":
            path = "/index.html"
        path = os.path.normpath(path).lstrip("/")
        full = os.path.join(ROOT, path)
        if not full.startswith(ROOT) or not os.path.isfile(full):
            self.send_error(404)
            return
        ctype = {
            ".html": "text/html; charset=utf-8",
            ".js": "application/javascript",
            ".css": "text/css",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".svg": "image/svg+xml",
            ".md": "text/plain; charset=utf-8",
        }.get(os.path.splitext(full)[1].lower(), "application/octet-stream")
        with open(full, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    srv = ThreadingHTTPServer((BIND_HOST, port), Handler)
    mode = "DRY-RUN（只写 feedback.log）" if DRY_RUN else "转发微信 -> %s" % HERMES_TARGET
    print("morse-trainer serving on %s:%d  |  feedback: %s" % (BIND_HOST, port, mode))
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
