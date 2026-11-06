"""从 match-centre 页面文本中解析比赛数据"""
import re
from models import Match, RankingEntry
from utils import log


def _normalize(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


# 过滤这些不是球员名的关键词
BAD_WORDS = {
    "Winner", "Frames", "Break", "Points", "Round", "Final", "Semi",
    "Quarter", "Match", "Session", "Live", "Results", "Draw", "Latest",
    "Stats", "Season", "Rankings", "Tournament", "International",
    "Championship", "Nanjing", "China", "November", "November",
    "More", "No", "Match No", "Fan", "Hossein", "Vafaei"  # 调试用，后续删
}


def parse_live_from_text(text: str) -> list[Match]:
    """
    match-centre 页面比分格式：
    "Si Jiahui 6 Frames 0 Liu Hongyu"
    或
    "Fan Zhengyi 14:00 Hossein Vafaei" (这是赛程，不是比分)
    """
    matches = []
    if not text:
        return matches

    text = _normalize(text)

    # 匹配比分格式：球员A 数字 Frames 数字 球员B
    score_pattern = re.compile(
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+"
        r"(\d{1,2})\s+Frames\s+(\d{1,2})\s+"
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)"
    )

    i = 0
    seen = set()
    for m in score_pattern.finditer(text):
        p1, s1, s2, p2 = m.groups()
        if p1 in BAD_WORDS or p2 in BAD_WORDS:
            continue
        key = (p1, p2)
        if key in seen:
            continue
        seen.add(key)

        match = Match(id=f"live_{i}")
        match.event_name = "国际锦标赛"
        match.event_tier = "ranking"
        match.status = "completed" if int(s1) > 0 or int(s2) > 0 else "live"
        match.player1 = {"name": p1, "score": int(s1)}
        match.player2 = {"name": p2, "score": int(s2)}
        matches.append(match)
        i += 1

    # 如果没匹配到 Frames 格式，试试赛程格式：球员A 时间 球员B
    if not matches:
        schedule_pattern = re.compile(
            r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+"
            r"(\d{1,2}:\d{2})\s+"
            r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)"
        )
        for m in schedule_pattern.finditer(text):
            p1, time, p2 = m.groups()
            if p1 in BAD_WORDS or p2 in BAD_WORDS:
                continue
            match = Match(id=f"sched_{i}")
            match.event_name = "国际锦标赛"
            match.event_tier = "ranking"
            match.status = "upcoming"
            match.scheduled_at = time
            match.player1 = {"name": p1, "score": None}
            match.player2 = {"name": p2, "score": None}
            matches.append(match)
            i += 1

    log.info(f"解析到 {len(matches)} 场比赛")
    return matches


def parse_rankings_from_text(text: str) -> list[RankingEntry]:
    return []
