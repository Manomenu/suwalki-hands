# ruff: noqa: E402
import logging

logging.getLogger("LiteLLM").setLevel(logging.ERROR)

from ebrit_hands_library.constants import LOGS_DIR
from ebrit_hands_library.log import setup_logging

setup_logging("ytrack_channel", LOGS_DIR)

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "ebrit_hands_ytrack_channel.app:app",
        host="0.0.0.0",
        port=6010,
        reload=False,
    )
