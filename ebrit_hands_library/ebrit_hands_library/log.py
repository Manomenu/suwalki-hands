import logging
from datetime import datetime, timedelta
from pathlib import Path

_OWN_PREFIXES = ("ebrit_hands",)


class _OwnCodeFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.name.startswith(_OWN_PREFIXES)


class _DateRotatingFileHandler(logging.FileHandler):
    """FileHandler that archives the log file when the date changes."""

    def __init__(self, logs_dir: Path, service: str, suffix: str, prefix: str = "", **kwargs):
        self._logs_dir = logs_dir
        self._service = service
        self._suffix = suffix
        self._prefix = prefix
        self._date = datetime.now().strftime("%Y-%m-%d")
        super().__init__(self._path_for(self._date), **kwargs)

    def _path_for(self, date: str) -> Path:
        return self._logs_dir / f"{self._prefix}{date}.{self._service}.{self._suffix}"

    def emit(self, record: logging.LogRecord) -> None:
        today = datetime.now().strftime("%Y-%m-%d")
        if today != self._date:
            old_path = self._path_for(self._date)
            self._date = today
            self.acquire()
            try:
                self.stream.close()
                archive_dir = self._logs_dir / "archive"
                archive_dir.mkdir(exist_ok=True)
                if old_path.exists():
                    old_path.rename(archive_dir / old_path.name)
                self.baseFilename = str(self._path_for(today))
                self.stream = self._open()
            finally:
                self.release()
        super().emit(record)


def setup_logging(service: str, logs_dir: Path = Path("logs")) -> None:
    logs_dir.mkdir(parents=True, exist_ok=True)

    cutoff = (datetime.now() - timedelta(days=7)).timestamp()
    for search_dir in [logs_dir, logs_dir / "archive"]:
        if search_dir.exists():
            for f in search_dir.glob("*.log"):
                if f.stat().st_mtime < cutoff:
                    f.unlink()

    fmt = logging.Formatter("%(asctime)s %(levelname)-8s %(name)s: %(message)s")

    info_handler = _DateRotatingFileHandler(logs_dir, service, "log", encoding="utf-8")
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(fmt)
    info_handler.addFilter(_OwnCodeFilter())

    debug_handler = _DateRotatingFileHandler(logs_dir, service, "log", prefix="debug.", encoding="utf-8")
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(fmt)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(info_handler)
    root.addHandler(debug_handler)
