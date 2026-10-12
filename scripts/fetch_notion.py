"""Pull every vendor from the Grade10 Notion vendor database into data/vendors.json.

Needs NOTION_TOKEN (an internal integration secret) with access to the Vendors database.
Uses only the Python standard library so the GitHub Action needs no installs.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DATABASE_ID = os.environ.get("NOTION_DATABASE_ID", "49fa0b1223ba40029382613ce1ca0998")
NOTION_VERSION = "2022-06-28"
OUT = Path(__file__).resolve().parent.parent / "data" / "vendors.json"

COLUMNS = [
    "Vendor", "Contact Person", "Instagram", "Email", "Contact Details", "Country", "Region",
    "Categories", "Vendor Type", "Price Range", "Lead Rating", "G10 Fest Interest",
    "G10 Consignment Interest", "Partnership Opportunity", "Notes / Market Insights",
    "Our Contact", "Met At", "Outreach Status", "Next Step",
]


def plain(prop):
    """Turn one Notion property value into plain text (lists become comma-separated)."""
    t = prop.get("type")
    v = prop.get(t)
    if v is None:
        return None
    if t in ("title", "rich_text"):
        return "".join(part.get("plain_text", "") for part in v) or None
    if t in ("select", "status"):
        return v.get("name")
    if t == "multi_select":
        return ", ".join(o["name"] for o in v) or None
    if t in ("url", "email", "phone_number"):
        return v or None
    if t == "date":
        return v.get("start")
    if t == "number":
        return v
    return None


def query(token):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    cursor = None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                page = json.load(resp)
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")
            sys.exit(f"Notion API error {e.code}: {detail}\n"
                     "Check that NOTION_TOKEN is set and the Vendors database is shared with the integration.")
        yield from page["results"]
        if not page.get("has_more"):
            return
        cursor = page["next_cursor"]


def main():
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        sys.exit("NOTION_TOKEN is not set. Add it under the repo's Settings > Secrets and variables > Actions.")
    rows = []
    for page in query(token):
        if page.get("archived") or page.get("in_trash"):
            continue
        props = page["properties"]
        row = {c: plain(props[c]) if c in props else None for c in COLUMNS}
        row["url"] = page.get("url")
        if row["Vendor"]:
            rows.append(row)
    rows.sort(key=lambda r: r["Vendor"].lower())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "updated": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "rows": rows,
    }, ensure_ascii=False, indent=1))
    print(f"Wrote {len(rows)} vendors to {OUT}")


if __name__ == "__main__":
    main()
