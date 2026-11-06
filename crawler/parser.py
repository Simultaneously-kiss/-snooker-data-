"""从页面文本中解析比赛数据（正则版，因为不知道 DOM 结构）"""
import re
from models import Match, RankingEntry, classify_event
from utils import log

def parse_live_from_text(text: str) -> list[Match]:
    """从页面文本里提取正在进行的比赛"""
    matches = []
    if not text:
        return matches

    # 匹配类似 "PlayerA 5 - 4 PlayerB" 的比分模式
    # 斯诺克比分通常是数字-数字，选手名是英文
    score_pattern = re.compile(
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+"
        r"(\d+)\s*[-–:]\s*(\d+)\s+"
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)"
    )

    for i, m in enumerate(score_pattern.finditer(text)):
        try:
            p1_name, s1, s2, p2_name = m.groups()
            match = Match(id=f"live_{i}")
            match.event_name = "WST 赛事"
            match.event_tier = "ranking"
            match.status = "live"
            match.player1 = {"name": p1_name, "score": int(s1)}
            match.player2 = {"name": p2_name, "score": int(s2)}
            matches.append(match)
        except Exception as e:
            log.warning(f"解析第 {i} 场失败: {e}")
            continue

    log.info(f"从文本中解析到 {len(matches)} 场比赛")
    return matches

def parse_rankings_from_text(text: str) -> list[RankingEntry]:
    """从页面文本中提取排名"""
    entries = []
    if not text:
        return entries

    # 排名表通常是：排名 球员名 国籍 积分
    # 先匹配 "数字 名字 数字" 的模式
    rank_pattern = re.compile(r"(\d+)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(\d[\d,]+)")

    for i, m in enumerate(rank_pattern.finditer(text)):
        try:
            rank, name, points = m.groups()
            entry = RankingEntry()
            entry.rank = int(rank)
            entry.name = name
            entry.points = int(points.replace(",", ""))
            entries.append(entry)
        except Exception as e:
            continue

    log.info(f"解析到 {len(entries)} 条排名")
    return entries
