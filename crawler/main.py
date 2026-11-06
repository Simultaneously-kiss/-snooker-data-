"""爬虫主入口"""
from utils import DATA_DIR, save_json, now_iso, log
from snooker_org import fetch_live_html, fetch_rankings_html
from parser import parse_live_from_html, parse_rankings_from_html


def run():
    log.info("开始抓取 snooker.org")

    live_html = fetch_live_html()
    live_matches = parse_live_from_html(live_html)
    save_json(DATA_DIR / "live.json", {
        "last_updated": now_iso(),
        "matches": [m.to_dict() for m in live_matches]
    })

    rank_html = fetch_rankings_html()
    rankings = parse_rankings_from_html(rank_html)
    save_json(DATA_DIR / "rankings-main.json", {
        "season": "2024/25",
        "type": "main",
        "updated_at": now_iso(),
        "entries": [e.to_dict() for e in rankings]
    })

    save_json(DATA_DIR / "today.json", {
        "last_updated": now_iso(),
        "date": now_iso()[:10],
        "matches": [m.to_dict() for m in live_matches]
    })

    save_json(DATA_DIR / "_meta.json", {
        "last_updated": now_iso(),
        "source": "snooker.org",
        "status": "ok"
    })

    log.info("抓取完成")


if __name__ == "__main__":
    run()
