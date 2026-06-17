# ebrit-hands

AI agent system that receives tasks (via YouTrack or HTTP) and autonomously implements them in a Git repository using OpenHands.

## Services

| Service | Port | Description |
|---|---|---|
| `ebrit_hands` | 6009 | Core agent — receives tasks, runs OpenHands, commits & creates MR |
| `ebrit_hands_ytrack_channel` | 6010 | YouTrack webhook receiver — forwards tasks to ebrit_hands |
| `ebrit_hands_web` | 6011 | Web UI — task board with status tracking |

## Quick Start

### 0. One-time host setup (local development only)

Services use `host.containers.internal` to reach each other across Docker and local debug without config changes. On Linux this hostname isn't added automatically, so add it once:

```bash
echo "127.0.0.1  host.containers.internal" | sudo tee -a /etc/hosts
```

macOS and Windows already resolve this automatically.

### 1. Configure environment

Create a root `.env` file (gitignored) with secrets:

```bash
# GitLab repos to work on (repeat GITLAB_REPO_N / GITLAB_TOKEN_N for more repos)
GITLAB_TOKEN_1=glpat-...

# Laminar observability — see step 2 below
LMNR_PROJECT_API_KEY=
```

Create per-service env files:

```bash
cp ebrit_hands_ytrack_channel/.env.example ebrit_hands_ytrack_channel/.env
# fill in: YOUTRACK_TOKEN (optional)
```

### 2. Set up Laminar observability (optional)

Laminar traces agent runs, LLM calls, and tool executions.

```bash
./scripts/laminar-up.sh
```

Then:
1. Open [http://localhost:5667](http://localhost:5667) and create an account
2. Go to **Settings → API Keys → Create** and copy the key
3. Paste it into `.env`:
   ```
   LMNR_PROJECT_API_KEY=<your key>
   ```

If `LMNR_PROJECT_API_KEY` is empty, Laminar is simply disabled — nothing breaks.

To stop Laminar: `./scripts/laminar-down.sh`

### 3. Sync dependencies

```bash
./scripts/sync.sh
```

### 4. Run

```bash
./scripts/run.sh                # starts ebrit_hands on :6009
./scripts/infrastructure-up.sh  # starts ytrack-channel + web UI via podman-compose
```

To see all available interfaces:

```bash
./scripts/print-links.sh
```

---

## Web UI

Task board for submitting and tracking AI tasks.

### Local development

```bash
cd ebrit_hands_web
cp .env.local.example .env.local
npm install
npm run dev
```

Open [http://localhost:6011](http://localhost:6011).

### Production

Included in `./scripts/infrastructure-up.sh` — the web UI starts automatically alongside ytrack-channel.

Available at [http://localhost:6011](http://localhost:6011).

### Usage

1. Click **+ New Task** — fill in Issue ID, Title, Branch, Description
2. Tab through fields, press **Submit Task**
3. Task card appears and tracks status: `Submitted → In Progress → Finished`
4. Click **×** on finished cards to remove them from the board
