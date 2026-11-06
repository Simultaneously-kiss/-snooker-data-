"""爬虫主入口：抓取 → 解析 → 生成 JSON"""
import json
from pathlib import Path
from datetime import datetime, timezone

from utils import DATA_DIR, save_json, load_json, now_iso, log
from wst import fetch_all
from parser import parse_live_matches, parse_schedule, parse_rankings


def run():
    log.info("=" * 50)
    log.info("开始抓取斯诺克数据")
    log.info("=" * 50)

    # 1. 抓取页面
    pages = fetch_all()

    # 2. 解析 + 生成 JSON
    # --- 正在进行的比赛 ---
    if "live" in pages:
        live_matches = parse_live_matches(pages["live"])
        save_json(DATA_DIR / "live.json", {
            "last_updated": now_iso(),
            "matches": [m.to_dict() for m in live_matches]
        })
    else:
        log.warning("live 页面未抓取成功，保留旧数据")

    # --- 今日赛程 ---
    if "schedule" in pages:
        schedule = parse_schedule(pages["schedule"])
        save_json(DATA_DIR / "today.json", {
            "last_updated": now_iso(),
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "matches": [m.to_dict() for m in schedule]
        })
    else:
        log.warning("schedule 页面未抓取成功，保留旧数据")

    # --- 世界排名 ---
    if "rankings" in pages:
        rankings = parse_rankings(pages["rankings"])
        save_json(DATA_DIR / "rankings-main.json", {
            "season": "2024/25",
            "type": "main",
            "updated_at": now_iso(),
            "entries": [e.to_dict() for e in rankings]
        })
    else:
        log.warning("rankings 页面未抓取成功，保留旧数据")

    # --- 元信息 ---
    save_json(DATA_DIR / "_meta.json", {
        "last_updated": now_iso(),
        "source": "wst.tv",
        "status": "ok"
    })

    log.info("=" * 50)
    log.info("抓取完成")
    log.info("=" * 50)


if __name__ == "__main__":
    run()
