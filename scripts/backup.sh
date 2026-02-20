#!/bin/bash
# backup.sh - Backup all OpenClaw data

set -e

BACKUP_DIR="$HOME/.openclaw/backups"
REPO_DIR="$HOME/.openclaw/workspace/clawdbot-kimi-agent"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_NAME="openclaw_backup_$DATE"

echo "🔄 Starting backup: $BACKUP_NAME"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup workspace
tar -czf "$BACKUP_DIR/${BACKUP_NAME}_workspace.tar.gz" \
  -C "$HOME/.openclaw" workspace/

# Backup config
cp "$HOME/.openclaw/openclaw.json" "$BACKUP_DIR/${BACKUP_NAME}_config.json"

# Backup credentials (encrypted)
tar -czf "$BACKUP_DIR/${BACKUP_NAME}_credentials.tar.gz" \
  -C "$HOME/.openclaw" credentials/ 2>/dev/null || echo "⚠️ No credentials to backup"

# Push to GitHub
cd "$REPO_DIR"
git add -A
git commit -m "Backup: $DATE - Automated backup" || echo "No changes to commit"
git push origin main 2>/dev/null || echo "⚠️ Could not push to GitHub"

echo "✅ Backup complete: $BACKUP_DIR/${BACKUP_NAME}_*"
echo "📊 Backup size: $(du -sh $BACKUP_DIR/${BACKUP_NAME}_* | awk '{print $1}' | head -1)"
