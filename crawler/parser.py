"""从页面文本中解析比赛数据（改进版，处理换行和误匹配）"""
import re
from models import Match, RankingEntry, classify_event
from utils import log


def _normalize(text: str) -> str:
    """把页面文本整理成单行，去掉多余换行和空格"""
    if not text:
        return ""
    # 多个换行/空格合并成一个空格
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_live_from_text(text: str) -> list[Match]:
    """从页面文本里提取正在进行的比赛"""
    matches = []
    if not text:
        return matches

    text = _normalize(text)

    # 过滤关键词：这些不是球员名
    bad_names = {"Winner", "Frames", "Break", "Points", "Round", "Final", "Semi",
                 "Quarter", "Match", "Session", "Live", "Results", "Draw"}

    # 匹配比分模式：名字 数字 - 数字 名字
    # 名字允许有空格（如 Kyren Wilson）
    score_pattern = re.compile(
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+"
        r"(\d{1,2})\s*[-–:]\s*(\d{1,2})\s+"
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)"
    )

    seen = set()
    i = 0
    for m in score_pattern.finditer(text):
        p1_name, s1, s2, p2_name = m.groups()

        # 过滤误匹配
        if p1_name in bad_names or p2_name in bad_names:
            continue
        if p1_name == p2_name:
            continue
        if int(s1) > 20 or int(s2) > 20:  # 斯诺克单场最多 35 局，过滤异常大数字
            continue

        key = (p1_name, p2_name, s1, s2)
        if key in seen:
            continue
        seen.add(key)

        match = Match(id=f"live_{i}")
        match.event_name = "WST 赛事"
        match.event_tier = "ranking"
        match.status = "live"
        match.player1 = {"name": p1_name, "score": int(s1)}
        match.player2 = {"name": p2_name, "score": int(s2)}
        matches.append(match)
        i += 1

    log.info(f"从文本中解析到 {len(matches)} 场比赛")
    return matches


def parse_rankings_from_text(text: str) -> list[RankingEntry]:
    """从页面文本中提取排名"""
    entries = []
    if not text:
        return entries

    text = _normalize(text)
    # 排名模式：数字 名字 数字（积分）
    rank_pattern = re.compile(r"\b(\d{1,2})\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(\d[\d,]+)\b")

    seen = set()
    for m in rank_pattern.finditer(text):
        rank, name, points = m.groups()
        if name in {"Winner", "Frames", "Break"}:
            continue
        if int(rank) > 200:  # 排名榜最多 100 多人
            continue
        if rank in seen:
            continue
        seen.add(rank)

        entry = RankingEntry()
        entry.rank = int(rank)
        entry.name = name
        entry.points = int(points.replace(",", ""))
        entries.append(entry)

    log.info(f"解析到 {len(entries)} 条排名")
    return entries
