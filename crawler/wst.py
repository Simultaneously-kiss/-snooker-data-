"""wst.tv 页面抓取（Playwright 版，直接访问 match-centre）"""
from playwright.sync_api import sync_playwright
from utils import log

# 当前正在进行的赛事：国际锦标赛
# 后续有新赛事时改这里的 UUID 就行
MATCH_CENTRE_URL = "https://www.wst.tv/match-centre/2689dd23-0001-41e3-8408-e047bb361803"


def fetch_page_text(url: str, wait_ms: int = 3000) -> str | None:
    """用 headless Chrome 打开页面，返回页面文本"""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            )
            log.info(f"打开页面: {url}")
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(wait_ms)
            text = page.inner_text("body")
            browser.close()
            return text
    except Exception as e:
        log.error(f"打开页面失败 {url}: {e}")
        return None


def fetch_live_text() -> str | None:
    """抓取赛事中心页面文本（含比分）"""
    return fetch_page_text(MATCH_CENTRE_URL)


def fetch_rankings_text() -> str | None:
    """排名页暂时返回空，后续再调"""
    return None
