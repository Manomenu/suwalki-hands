# ruff: noqa: E402
import logging
import os

os.environ["OPENHANDS_SUPPRESS_BANNER"] = "1"

logging.getLogger("LiteLLM").setLevel(logging.ERROR)

from ebrit_hands_library.constants import LOGS_DIR
from ebrit_hands_library.log import setup_logging

setup_logging("ebrit_hands", LOGS_DIR)

from ebrit_hands.settings import settings

if settings.lmnr_project_api_key:
    logging.getLogger("lmnr.sdk.laminar").setLevel(logging.WARNING)
    from lmnr import Laminar
    Laminar.initialize(
        project_api_key=settings.lmnr_project_api_key,
        instruments=set(),
        base_url=settings.lmnr_base_url,
        http_port=settings.lmnr_http_port,
        grpc_port=settings.lmnr_grpc_port,
    )

import subprocess
from pathlib import Path
import uvicorn

if __name__ == "__main__":
    subprocess.run(
        [Path(__file__).parent.parent.parent / "scripts" / "cleanup.sh"],
        check=True,
    )
    uvicorn.run(
        "ebrit_hands.app:app",
        host="0.0.0.0",
        port=6009,
        reload=False,
    )
