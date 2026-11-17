"""Tiny Chrome DevTools driver using Quarto's chrome-headless-shell. Dev/test only."""
import glob, http.server, json, os, socketserver, subprocess, threading, time, urllib.request
from pathlib import Path
import websocket

def chrome_path():
    pats = [str(Path.home() / "Library/Application Support/quarto/chrome-headless-shell/*/chrome-headless-shell"),
            str(Path.home() / ".local/share/quarto/chrome-headless-shell/*/chrome-headless-shell")]
    for p in pats:
        hits = glob.glob(p)
        if hits: return hits[0]
    raise SystemExit("chrome-headless-shell not found: run `quarto install chrome-headless-shell`")

def serve(directory, port):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=str(directory), **k)
        def log_message(self, *a): pass
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(("127.0.0.1", port), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv

KEYS = {"ArrowLeft": 37, "ArrowUp": 38, "ArrowRight": 39, "ArrowDown": 40, "Enter": 13, " ": 32}

class Browser:
    def __init__(self, width=1280, height=900, port=9333):
        self.proc = subprocess.Popen([chrome_path(), "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
            f"--remote-debugging-port={port}", f"--window-size={width},{height}", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(50):
            try:
                tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json")); break
            except Exception: time.sleep(0.2)
        self.ws = websocket.create_connection(next(t for t in tabs if t["type"] == "page")["webSocketDebuggerUrl"])
        self.n = 0
        self.cmd("Page.enable"); self.cmd("Emulation.setDeviceMetricsOverride", width=width, height=height, deviceScaleFactor=1, mobile=False)
    def cmd(self, method, **params):
        self.n += 1; self.ws.send(json.dumps({"id": self.n, "method": method, "params": params}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get("id") == self.n: return m.get("result", {})
    def go(self, url, wait=1.2):
        self.cmd("Page.navigate", url=url); time.sleep(wait)
    def js(self, expr):
        r = self.cmd("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True)
        if "exceptionDetails" in r: raise RuntimeError(r["exceptionDetails"].get("exception", {}).get("description", "js error"))
        return r["result"].get("value")
    def press(self, key, wait=0.15):
        code = KEYS[key] if key in KEYS else ord(key.upper())
        text = key if len(key) == 1 else ("\r" if key == "Enter" else "")
        for t in ("keyDown", "keyUp"):
            self.cmd("Input.dispatchKeyEvent", type=t, key=key, windowsVirtualKeyCode=code, text=text if t == "keyDown" else "")
        time.sleep(wait)
    def click_text(self, text, sel="button"):
        return self.js("(() => { const b=[...document.querySelectorAll(%r)].find(e=>e.textContent.includes(%r) && !e.hidden); if(!b) return false; b.click(); return true; })()" % (sel, text))
    def shot(self, path):
        import base64
        Path(path).write_bytes(base64.b64decode(self.cmd("Page.captureScreenshot", format="png")["data"]))
    def close(self):
        try: self.ws.close()
        finally: self.proc.terminate()
