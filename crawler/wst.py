"""wst.tv 页面抓取（Playwright headless Chrome 版）"""
from playwright.sync_api import sync_playwright
from utils import log, now_iso

# 入口 URL：WST 官网首页，从这里找 live/match-centre 链接
WST_HOME = "https://www.wst.tv/"

def fetch_page_text(url: str, wait_selector: str = "body") -> str | None:
    """用 headless Chrome 打开页面，返回页面文本"""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            )
            log.info(f"打开页面: {url}")
            page.goto(url, wait_until="networkidle", timeout=30000)
            # 等页面渲染完
            page.wait_for_timeout(2000)
            text = page.inner_text("body")
            browser.close()
            return text
    except Exception as e:
        log.error(f"打开页面失败 {url}: {e}")
        return None

def fetch_live_text() -> str | None:
    """抓取正在进行的比赛页面文本"""
    # 先访问首页，找 Match Centre 链接
    home_text = fetch_page_text(WST_HOME)
    if not home_text:
        return None

    # 尝试直接访问 match-centre 列表页
    # 如果首页找不到，就用一个已知的进行中赛事 URL
    # 这里先返回首页文本，后续根据日志调整
    return home_text

def fetch_rankings_text() -> str | None:
    """抓取排名页面文本"""
    # WST 排名页 URL 待确认，先试常见路径
    return fetch_page_text("https://www.wst.tv/rankings/")
