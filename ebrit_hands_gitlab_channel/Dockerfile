FROM python:3.12-slim

WORKDIR /app

RUN pip install uv --no-cache-dir

COPY ebrit_hands_library ./ebrit_hands_library
COPY ebrit_hands_gitlab_channel ./ebrit_hands_gitlab_channel

RUN cd ebrit_hands_gitlab_channel && uv sync --no-dev

EXPOSE 5085

CMD ["ebrit_hands_gitlab_channel/.venv/bin/python", "-m", "ebrit_hands_gitlab_channel"]
