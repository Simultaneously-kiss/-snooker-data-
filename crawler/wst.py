"""wst.tv 页面抓取入口"""
from utils import get_client, fetch_url, log

# 目标 URL（根据实际 wst.tv 站点结构调整）
WST_URLS = {
    "live": "https://wst.tv/live-scores/",
    "schedule": "https://wst.tv/schedule/",
    "rankings": "https://wst.tv/rankings/",
}


def fetch_all():
    """抓取所有目标页面，返回 {key: html_content}"""
    client = get_client()
    results = {}

    for key, url in WST_URLS.items():
        html = fetch_url(client, url)
        if html:
            results[key] = html
        else:
            log.error(f"{key} 页面抓取失败")

    client.close()
    return results
