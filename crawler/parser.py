"""HTML 解析器：把 wst.tv 的 HTML 转成结构化数据

⚠️ 注意：以下 CSS 选择器是基于斯诺克赛事网站常见结构推测的。
   第一次跑如果解析不到数据，请打开 wst.tv 实际页面，
   F12 检查元素，调整下面的选择器即可。
"""
import re
from selectolax.lexbor import LexborHTMLParser as HTMLParser

from models import Match, PlayerScore, RankingEntry, classify_event
from utils import log


# ============ 选择器配置（调试时改这里就行） ============

# 正在比赛列表：每个比赛卡片的容器
LIVE_MATCH_SELECTOR = ".live-score-card, .match-live, .scoreboard-item"
# 赛程列表
SCHEDULE_MATCH_SELECTOR = ".schedule-item, .fixture, .match-card"
# 排名表格行
RANKING_ROW_SELECTOR = ".rankings-table tbody tr, .ranking-row"


# ============ 解析函数 ============

def parse_live_matches(html: str) -> list[Match]:
    """解析正在进行的比赛页面"""
    tree = HTMLParser(html)
    matches = []

    # 尝试多种常见选择器
    cards = tree.css(LIVE_MATCH_SELECTOR)
    if not cards:
        log.warning("未找到正在比赛的卡片，可能选择器需要调整")
        return []

    for i, card in enumerate(cards):
        try:
            match = Match(id=f"live_{i}")

            # 赛事名
            event_el = card.css_first(".event-name, .tournament, h3, h4")
            if event_el:
                match.event_name = event_el.text(strip=True)
                match.event_tier = classify_event(match.event_name)

            # 轮次
            round_el = card.css_first(".round, .stage")
            if round_el:
                match.round = round_el.text(strip=True)

            # 比分 - 尝试常见结构
            score_text = card.text(strip=True)
            # 匹配类似 "Trump 5 - 4 O'Sullivan" 的模式
            score_match = re.search(r"([A-Z][a-z]+)\s+(\d+)\s*[-–:]\s*(\d+)\s*([A-Z][a-z']+)", score_text)
            if score_match:
                match.player1 = {"name": score_match.group(1), "score": int(score_match.group(2))}
                match.player2 = {"name": score_match.group(4), "score": int(score_match.group(3))}
                match.status = "live"

            # 单杆最高分
            break_match = re.search(r"[Bb]reak[:\s]*(\d+)", score_text)
            if break_match:
                match.highest_break = int(break_match.group(1))

            if match.player1 and match.player2:
                matches.append(match)
        except Exception as e:
            log.warning(f"解析第 {i} 个比赛卡片失败: {e}")
            continue

    log.info(f"解析到 {len(matches)} 场正在进行的比赛")
    return matches


def parse_schedule(html: str) -> list[Match]:
    """解析赛程页面"""
    tree = HTMLParser(html)
    matches = []

    cards = tree.css(SCHEDULE_MATCH_SELECTOR)
    if not cards:
        log.warning("未找到赛程条目，可能选择器需要调整")
        return []

    for i, card in enumerate(cards):
        try:
            match = Match(id=f"sched_{i}")

            # 时间
            time_el = card.css_first(".time, .kickoff, .datetime")
            if time_el:
                match.scheduled_at = time_el.text(strip=True)

            # 赛事名
            event_el = card.css_first(".event, .tournament-name")
            if event_el:
                match.event_name = event_el.text(strip=True)
                match.event_tier = classify_event(match.event_name)

            # 对阵双方
            players = card.css(".player, .opponent, .team-name")
            if len(players) >= 2:
                match.player1 = {"name": players[0].text(strip=True)}
                match.player2 = {"name": players[1].text(strip=True)}

            match.status = "upcoming"
            matches.append(match)
        except Exception as e:
            log.warning(f"解析第 {i} 个赛程条目失败: {e}")
            continue

    log.info(f"解析到 {len(matches)} 场赛程")
    return matches


def parse_rankings(html: str) -> list[RankingEntry]:
    """解析世界排名表格"""
    tree = HTMLParser(html)
    entries = []

    rows = tree.css(RANKING_ROW_SELECTOR)
    if not rows:
        log.warning("未找到排名表格行，可能选择器需要调整")
        return []

    for i, row in enumerate(rows):
        try:
            cells = row.css("td")
            if len(cells) < 4:
                continue

            entry = RankingEntry()
            entry.rank = _safe_int(cells[0].text(strip=True))
            entry.name = cells[1].text(strip=True)

            # 国籍可能在第二个单元格里，需要看实际页面结构
            if len(cells) >= 3:
                entry.nationality = cells[2].text(strip=True)
            if len(cells) >= 4:
                entry.points = _safe_int(cells[3].text(strip=True).replace(",", ""))

            entries.append(entry)
        except Exception as e:
            log.warning(f"解析第 {i} 行排名失败: {e}")
            continue

    log.info(f"解析到 {len(entries)} 条排名")
    return entries


def _safe_int(text: str) -> int:
    """安全转整数，失败返回 0"""
    try:
        return int(re.sub(r"[^\d]", "", text))
    except (ValueError, TypeError):
        return 0
