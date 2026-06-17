import openhands.workspace.docker.workspace as _docker_ws_module
from openhands.workspace import DockerWorkspace


class UserDockerWorkspace(DockerWorkspace):
    """DockerWorkspace that forces container root so bind-mount files are owned by the host user (rootless Podman: uid 0 in container = host user on filesystem)."""

    def model_post_init(self, context):
        orig = _docker_ws_module.execute_command

        def _patched(cmd, **kwargs):
            if cmd and cmd[0] == "docker" and len(cmd) > 1 and cmd[1] == "run":
                cmd = list(cmd)
                cmd.insert(2, "--user")
                cmd.insert(3, "0")
            return orig(cmd, **kwargs)

        _docker_ws_module.execute_command = _patched
        try:
            super().model_post_init(context)
        finally:
            _docker_ws_module.execute_command = orig
