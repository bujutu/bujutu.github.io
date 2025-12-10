import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from jinja2 import Template

BASE_URL = "https://paypay.ne.jp/event/support-local/"

POST_PATH = "_posts/paypay-campaigns.md"
TEMPLATE_PATH = "scripts/template_paypay_post.md.j2"


def extract_rate(text):
    """
    「数字＋％付与」を探し、数字を返す。
    """
    pattern = r"(\d+(?:\.\d+)?)\s*％付与"
    m = re.search(pattern, text)
    return m.group(1) + "%" if m else "不明"


def get_campaign_rate(detail_url):
    """
    自治体ページにアクセスし、「％付与」直前の数字を抽出する。
    """
    try:
        html = requests.get(detail_url, timeout=10).text
        rate = extract_rate(html)
        return rate
    except Exception:
        return "要確認"


def fetch_campaigns():
    """
    メインページから自治体キャンペーンを抽出
    """
    html = requests.get(BASE_URL).text
    soup = BeautifulSoup(html, "html.parser")

    rows = soup.select("tr.supportLocal__row")

    campaigns = []

    for row in rows:
        link_tag = row.select_one("a.supportLocal__link")
        if not link_tag:
            continue

        url = link_tag.get("href")
        if ((not url.startswith("https://paypay.ne.jp/event/") \
            and not url.startswith("https://paypay.ne.jp/notice/")) \
            or "voucher" in url):
            continue

        # 1. 自治体名の抽出（スペースがあれば前半だけ）
        full_name = link_tag.text.strip()
        name = full_name.split(" ")[0]

        # 2. 状態（開催中 or 開催予定）
        status_tag = row.select_one(".supportLocal__label--green")
        if not status_tag:
            status = "開催中"
        else:
            status = status_tag.text.strip()

        # 3. 期間
        date_tag = row.select_one("p.supportLocal__date")
        period = date_tag.text.strip() if date_tag else "不明"

        # 4. 還元率抽出
        rate = get_campaign_rate(url)

        campaigns.append({
            "name": name,
            "status": status,
            "period": period,
            "rate": rate,
            "url": url
        })

    return campaigns


def render_markdown(campaigns):
    """
    Jinja2でMarkdownを生成
    """
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template = Template(f.read())

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rendered = template.render(
        campaigns=campaigns,
        now=now
    )

    with open(POST_PATH, "w", encoding="utf-8") as f:
        f.write(rendered)


if __name__ == "__main__":
    campaigns = fetch_campaigns()
    render_markdown(campaigns)
