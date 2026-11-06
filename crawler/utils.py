"""通用工具：日志、文件读写"""
import json
import logging
from pathlib import Path
from datetime import timezone

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("snooker-crawler")


def load_json(path: Path, default=None):
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log.warning(f"读取 {path} 失败: {e}")
        return default


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log.info(f"已写入: {path}")


def now_iso() -> str:
    from datetime import datetime
    return datetime.now(timezone.utc).isoformat()
