"""数据结构定义（对应前端 JSON Schema）"""
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class PlayerScore:
    id: str = ""
    name: str = ""
    full_name: str = ""
    score: Optional[int] = None


@dataclass
class Match:
    id: str = ""
    event_name: str = ""
    event_tier: str = "ranking"  # triple_crown / ranking / invitation / qualifier
    round: str = ""
    status: str = "upcoming"  # live / upcoming / completed
    session: str = ""
    best_of: int = 0
    player1: dict = field(default_factory=dict)
    player2: dict = field(default_factory=dict)
    highest_break: Optional[int] = None
    highest_break_player: str = ""
    scheduled_at: str = ""
    started_at: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class RankingEntry:
    rank: int = 0
    previous_rank: int = 0
    player_id: str = ""
    name: str = ""
    nationality: str = ""
    points: int = 0
    tournaments_played: int = 0

    def to_dict(self):
        return asdict(self)


# 赛事分类映射（根据赛事名关键词判断）
EVENT_TIER_RULES = [
    # (关键词列表, tier)
    (["World Championship", "World Snooker Championship"], "triple_crown"),
    (["UK Championship", "British Open"], "triple_crown"),
    (["Masters"], "triple_crown"),
    (["Qualifiers", "Qualifying"], "qualifier"),
    (["Champion of Champions", "Masters"], "invitation"),
]


def classify_event(event_name: str) -> str:
    """根据赛事名判断赛事等级"""
    name_lower = event_name.lower()
    for keywords, tier in EVENT_TIER_RULES:
        for kw in keywords:
            if kw.lower() in name_lower:
                return tier
    return "ranking"
