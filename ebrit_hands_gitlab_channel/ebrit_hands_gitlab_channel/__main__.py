# ruff: noqa: E402
import logging

from ebrit_hands_library.constants import LOGS_DIR
from ebrit_hands_library.log import setup_logging

setup_logging("gitlab_channel", LOGS_DIR)

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "ebrit_hands_gitlab_channel.app:app",
        host="0.0.0.0",
        port=5085,
        reload=False,
    )
