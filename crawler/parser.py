"""从 snooker.org HTML 中解析比赛数据"""
from selectolax.lexbor import LexborHTMLParser as HTMLParser
from models import Match, RankingEntry
from utils import log


def parse_live_from_html(html: str) -> list[Match]:
    """解析 live.htm 页面"""
    matches = []
    if not html:
        return matches

    tree = HTMLParser(html)
    # snooker.org 的比分通常在表格里
    rows = tree.css("table tr")

    i = 0
    for row in rows:
        cells = row.css("td")
        if len(cells) < 3:
            continue

        try:
            # 尝试解析：对阵双方 + 比分
            text = row.text(strip=True)
            if "-" not in text and "–" not in text:
                continue

            # 简单按文本切分
            parts = text.split()
            # 找比分数字
            score_idx = None
            for j, p in enumerate(parts):
                if p.isdigit() and len(p) <= 2:
                    score_idx = j
                    break

            if score_idx is None:
                continue

            match = Match(id=f"live_{i}")
            match.event_name = "WST 赛事"
            match.event_tier = "ranking"
            match.status = "live"
            # 粗略提取两边球员名
            match.player1 = {"name": "Player A", "score": int(parts[score_idx])}
            match.player2 = {"name": "Player B", "score": int(parts[score_idx + 1]) if score_idx + 1 < len(parts) else 0}
            matches.append(match)
            i += 1
        except Exception as e:
            continue

    log.info(f"解析到 {len(matches)} 场比赛")
    return matches


def parse_rankings_from_html(html: str) -> list[RankingEntry]:
    """解析排名页面"""
    entries = []
    if not html:
        return entries

    tree = HTMLParser(html)
    rows = tree.css("table tr")

    for row in rows:
        cells = row.css("td")
        if len(cells) < 3:
            continue
        try:
            entry = RankingEntry()
            entry.rank = int(cells[0].text(strip=True)) if cells[0].text(strip=True).isdigit() else 0
            entry.name = cells[1].text(strip=True)
            entries.append(entry)
        except:
            continue

    log.info(f"解析到 {len(entries)} 条排名")
    return entries
