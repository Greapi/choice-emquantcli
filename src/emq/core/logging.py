from __future__ import annotations

import logging


def setup_logging(level: str = "INFO", log_file: str | None = None) -> None:
    resolved_level = getattr(logging, level.upper(), logging.INFO)
    log_format = "%(asctime)s %(levelname)s %(name)s %(message)s"
    if log_file:
        logging.basicConfig(level=resolved_level, format=log_format, filename=log_file)
        return
    logging.basicConfig(level=resolved_level, format=log_format)
