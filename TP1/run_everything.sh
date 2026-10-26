#!/usr/bin/env bash
set -euo pipefail

SESSION="tp1"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v tmux >/dev/null 2>&1; then
    printf 'Error: tmux is required to run this script.\n' >&2
    exit 1
fi

if tmux has-session -t "$SESSION" 2>/dev/null; then
    if [[ -n "${TMUX:-}" ]]; then
        exec tmux switch-client -t "$SESSION"
    else
        exec tmux attach-session -t "$SESSION"
    fi
fi

tmux new-session -d -s "$SESSION" -n "TP1" -c "$SCRIPT_DIR"
SERVER_PANE="$(tmux display-message -p -t "$SESSION:0.0" '#{pane_id}')"
CLIENT_PANE="$(tmux split-window -h -t "$SERVER_PANE" -c "$SCRIPT_DIR" -P -F '#{pane_id}')"
TEMP_PANE="$(tmux split-window -v -t "$SERVER_PANE" -c "$SCRIPT_DIR" -P -F '#{pane_id}')"
HUM_PANE="$(tmux split-window -v -t "$CLIENT_PANE" -c "$SCRIPT_DIR" -P -F '#{pane_id}')"

tmux select-layout -t "$SESSION:0" tiled
tmux set-option -w -t "$SESSION:0" pane-border-status top
tmux set-option -w -t "$SESSION:0" pane-border-format '#T'

tmux select-pane -t "$SERVER_PANE" -T "server"
tmux select-pane -t "$CLIENT_PANE" -T "client"
tmux select-pane -t "$TEMP_PANE" -T "temp"
tmux select-pane -t "$HUM_PANE" -T "hum"

tmux send-keys -t "$SERVER_PANE" 'python3 server.py' C-m
tmux send-keys -t "$CLIENT_PANE" 'python3 client.py' C-m
tmux send-keys -t "$TEMP_PANE" 'python3 sensor.py temp' C-m
tmux send-keys -t "$HUM_PANE" 'python3 sensor.py hum' C-m

if [[ -n "${TMUX:-}" ]]; then
    exec tmux switch-client -t "$SESSION"
else
    exec tmux attach-session -t "$SESSION"
fi
