"""通用工具：HTTP 请求、限速、日志、文件读写"""
import time
import json
import os
import logging
from pathlib import Path
from datetime import datetime, timezone

import httpx

# 项目根目录
ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"

# 浏览器 UA，避免被反爬识别为爬虫
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

# 请求间隔（秒），对 wst.tv 友好
REQUEST_DELAY = 4.0

# 日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("snooker-crawler")


def get_client() -> httpx.Client:
    """创建一个带真实 UA 的 HTTP 客户端"""
    return httpx.Client(
        headers={"User-Agent": BROWSER_UA, "Accept-Language": "en-US,en;q=0.9"},
        timeout=30.0,
        follow_redirects=True,
    )


def fetch_url(client: httpx.Client, url: str) -> str | None:
    """带限速和重试的抓取"""
    for attempt in range(3):
        try:
            log.info(f"抓取: {url} (第{attempt+1}次)")
            resp = client.get(url)
            resp.raise_for_status()
            time.sleep(REQUEST_DELAY)
            return resp.text
        except Exception as e:
            log.warning(f"抓取失败: {e}")
            # 指数退避
            time.sleep(2 ** attempt)
    log.error(f"最终失败: {url}")
    return None


def load_json(path: Path, default=None):
    """读取 JSON，不存在或损坏时返回 default"""
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log.warning(f"读取 {path} 失败: {e}，使用旧数据")
        return default


def save_json(path: Path, data):
    """写入 JSON，确保目录存在"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log.info(f"已写入: {path}")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
