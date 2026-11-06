"""爬虫主入口：抓取 → 解析 → 生成 JSON"""
from utils import DATA_DIR, save_json, now_iso, log
from wst import fetch_live_text, fetch_rankings_text
from parser import parse_live_from_text, parse_rankings_from_text


def run():
    log.info("=" * 50)
    log.info("开始抓取斯诺克数据（Playwright 版）")
    log.info("=" * 50)

    # 抓取正在比赛
    live_text = fetch_live_text()
    live_matches = parse_live_from_text(live_text) if live_text else []
    save_json(DATA_DIR / "live.json", {
        "last_updated": now_iso(),
        "matches": [m.to_dict() for m in live_matches]
    })
    log.info(f"live.json: {len(live_matches)} 场比赛")

    # 抓取排名
    rank_text = fetch_rankings_text()
    rankings = parse_rankings_from_text(rank_text) if rank_text else []
    save_json(DATA_DIR / "rankings-main.json", {
        "season": "2024/25",
        "type": "main",
        "updated_at": now_iso(),
        "entries": [e.to_dict() for e in rankings]
    })
    log.info(f"rankings-main.json: {len(rankings)} 条排名")

    # 今日赛程（暂时复用 live 数据）
    save_json(DATA_DIR / "today.json", {
        "last_updated": now_iso(),
        "date": now_iso()[:10],
        "matches": [m.to_dict() for m in live_matches]
    })

    # 元信息
    save_json(DATA_DIR / "_meta.json", {
        "last_updated": now_iso(),
        "source": "wst.tv (playwright)",
        "status": "ok"
    })

    log.info("=" * 50)
    log.info("抓取完成")
    log.info("=" * 50)


if __name__ == "__main__":
    run()
