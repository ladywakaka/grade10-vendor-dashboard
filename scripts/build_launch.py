"""Embed data/launch.json into src/launch.html and write build/launch/index.html.

The output is the unencrypted page. The GitHub Action encrypts it with StatiCrypt
before publishing, so build/ must never be committed or deployed as is.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
template = (ROOT / "src" / "launch.html").read_text()
data = json.loads((ROOT / "data" / "launch.json").read_text())

# Escape "</" so text from Notion can never close the <script> tag that holds the data.
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
html = template.replace("__LAUNCH_DATA__", payload)

out = ROOT / "build" / "launch" / "index.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(html)
print(f"Built {out} with {len(data['activations'])} activations")
