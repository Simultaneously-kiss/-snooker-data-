"""snooker.org 页面抓取（传统 HTML，好爬）"""
import httpx
import time
from utils import log

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

# snooker.org 的页面 URL
LIVE_URL = "https://snooker.org/live.htm"
RESULTS_URL = "https://snooker.org/results.htm"
RANKINGS_URL = "https://snooker.org/rankings.htm"


def fetch_page(url: str) -> str | None:
    try:
        log.info(f"抓取: {url}")
        resp = httpx.get(url, headers=HEADERS, timeout=30.0, follow_redirects=True)
        resp.raise_for_status()
        time.sleep(3)  # 礼貌延迟
        return resp.text
    except Exception as e:
        log.error(f"抓取失败 {url}: {e}")
        return None


def fetch_live_html() -> str | None:
    return fetch_page(LIVE_URL)


def fetch_rankings_html() -> str | None:
    return fetch_page(RANKINGS_URL)
