#!/usr/bin/env python3
"""앱 화면 캡처 — headless Chrome로 PWA 주요 화면을 PNG로 저장.

기획서·README·스토어용 스크린샷을 재현 가능하게 생성한다.
사전조건: 정적 서버 실행(python3 scripts/serve.py) — 기본 http://localhost:5183
사용: python3 scripts/capture_screens.py [base_url]
"""
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.parse

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5183"
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "screens")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

Q = urllib.parse.quote("라면 어디에 수출하면 좋을까?")
# headless Chrome는 최소 창 너비 500px를 강제하므로 폰 화면은 500px로 캡처한다.
SHOTS = [
    ("01-home.png",    f"{BASE}/index.html",                                    (500, 1000)),
    ("02-radar.png",   f"{BASE}/index.html?tab=radar",                          (500, 1000)),
    ("03-advisor.png", f"{BASE}/index.html?tab=advisor&q={Q}",                  (500, 1000)),
    ("04-report.png",  f"{BASE}/index.html?tab=report&hs=1212.21&cc=US",        (500, 1040)),
    ("05-dashboard.png", f"{BASE}/dashboard.html",                              (1280, 880)),
    ("06-landing.png", f"{BASE}/home.html",                                     (1280, 980)),
]


def capture(name, url, size):
    prof = tempfile.mkdtemp()
    proc = None
    try:
        proc = subprocess.Popen([
            CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
            "--no-default-browser-check", f"--user-data-dir={prof}",
            "--hide-scrollbars", "--force-device-scale-factor=2",
            f"--window-size={size[0]},{size[1]}", "--virtual-time-budget=4000",
            f"--screenshot={os.path.join(OUT, name)}", url,
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            proc.wait(timeout=18)
        except subprocess.TimeoutExpired:
            proc.kill()  # headless 종료 플레이크 — 캡처는 이미 됨, 강제 종료 후 계속
    finally:
        if proc and proc.poll() is None:
            proc.kill()
        shutil.rmtree(prof, ignore_errors=True)
    p = os.path.join(OUT, name)
    print(f"  {name:18s} {'OK' if os.path.exists(p) else 'MISSING':8s} {url}")


def main():
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[2] if len(sys.argv) > 2 else None
    for name, url, size in SHOTS:
        if only and only not in name:
            continue
        capture(name, url, size)


if __name__ == "__main__":
    main()
