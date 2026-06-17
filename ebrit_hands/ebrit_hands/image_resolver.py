from ebrit_hands.settings import settings

_DEFAULT_SERVER_IMAGE = "ghcr.io/openhands/agent-server:latest-python"


def resolve_server_image(name: str) -> str:
    if name == "default":
        return _DEFAULT_SERVER_IMAGE
    return f"{settings.image_registry}:{name}"
