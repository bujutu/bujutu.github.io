#!/usr/bin/env python3
import os
import sys
import json
from datetime import datetime
import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape

DEFAULT_API = "https://www.paypay.ne.jp/opa-api/campaign/list/"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def fetch_campaigns(api_url):
    try:
        resp = requests.get(api_url, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error fetching: {e}", file=sys.stderr)
        return None

def normalize(item):
    return {
        "title": item.get("title") or item.get("campaignName") or "",
        "municipality": item.get("municipality") or item.get("city") or "",
        "start": item.get("startDate") or "",
        "end": item.get("endDate") or "",
        "rate": item.get("paybackRate") or "",
        "note": item.get("note") or "",
        "raw": item
    }

def extract_campaigns(api_json):
    if api_json is None:
        return []
    if isinstance(api_json, dict):
        for k in ["campaigns", "items", "data", "result", "campaignList"]:
            if k in api_json and isinstance(api_json[k], list):
                return [normalize(i) for i in api_json[k]]
    if isinstance(api_json, list):
        return [normalize(i) for i in api_json]
    return []

def main():
    api_url = os.environ.get("PAYPAY_API_URL", DEFAULT_API)

    # Jekyll 形式の固定記事ファイル
    output_path = os.path.join(
        os.path.dirname(SCRIPT_DIR),
        "_posts",
        "2025-12-05-paypay-campaigns.md"
    )

    template_path = os.path.join(SCRIPT_DIR, "template_post.md.j2")

    print("Fetching PayPay campaigns...")
    data = fetch_campaigns(api_url)
    campaigns = extract_campaigns(data)

    env = Environment(
        loader=FileSystemLoader(os.path.dirname(template_path)),
        autoescape=select_autoescape([])
    )
    template = env.get_template(os.path.basename(template_path))

    content = template.render(
        campaigns=campaigns,
        generated_at=datetime.now().isoformat()
    )

    # 旧内容と比較して変化なければコミットしない
    if os.path.exists(output_path):
        old = open(output_path, "r", encoding="utf-8").read()
        if old == content:
            print("No changes detected.")
            return

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Updated:", output_path)


if __name__ == "__main__":
    main()
