#!/bin/bash
# cleanup.sh - Clean up old session logs

set -e

DAYS=${1:-30}
SESSIONS_DIR="$HOME/.openclaw/workspace/clawdbot-kimi-agent/sessions/logs"
ARCHIVE_DIR="$HOME/.openclaw/workspace/clawdbot-kimi-agent/sessions/archive"

echo "🧹 Cleaning up sessions older than $DAYS days"

# Create archive directory
mkdir -p "$ARCHIVE_DIR"

# Find and archive old sessions
find "$SESSIONS_DIR" -type d -name "202*" -mtime +$DAYS | while read dir; do
    dirname=$(basename "$dir")
    echo "📦 Archiving: $dirname"
    tar -czf "$ARCHIVE_DIR/${dirname}.tar.gz" -C "$SESSIONS_DIR" "$dirname"
    rm -rf "$dir"
done

echo "✅ Cleanup complete"
echo "📦 Archives in: $ARCHIVE_DIR"
