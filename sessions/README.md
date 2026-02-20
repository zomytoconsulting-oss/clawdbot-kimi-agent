# 📊 Session Logging System

## Log Structure

```
sessions/
├── 2026-02-20/
│   ├── 15-57-00-agent-main.jsonl      # Raw transcript
│   ├── 15-57-00-summary.md            # Human summary
│   ├── 16-10-00-telegram-7861.jsonl   # Telegram session
│   └── stats.json                     # Session statistics
└── archive/
    └── 2026-01/                       # Monthly archive
```

## Log Format (JSONL)

```json
{"timestamp": "2026-02-20T15:57:00Z", "role": "user", "content": "...", "channel": "telegram"}
{"timestamp": "2026-02-20T15:57:05Z", "role": "assistant", "content": "...", "model": "k2p5"}
```

## Summary Format (Markdown)

```markdown
# Session 2026-02-20 15:57

## Channels Used
- Telegram (7861184420)
- WebChat

## Topics Discussed
1. Initial setup
2. Browser relay configuration
3. Telegram connection

## Tools Used
- browser
- gateway
- exec

## Files Created
- TOOLS.md (updated)
- BOOTSTRAP.md (deleted)

## Next Actions
- [ ] Test SerpAPI
- [ ] Continue 11880 scraping
```

## Retention Policy

| Age | Action |
|-----|--------|
| 0-7 days | Keep full logs |
| 8-30 days | Keep summaries only |
| 31-90 days | Archive to compressed storage |
| 90+ days | Delete (unless flagged) |

## Context Limit Monitoring

### Check Current Usage
```bash
openclaw status | grep -i "context\|tokens"
```

### Warning Levels
- 🟢 **< 150k:** Safe
- 🟡 **150k-200k:** Monitor
- 🟠 **200k-240k:** Summarize soon
- 🔴 **> 240k:** Critical - summarize NOW

## Automation

### Daily Cleanup (Cron)
```bash
# Run at 3 AM daily
0 3 * * * /path/to/cleanup.sh --days 30
```

### Weekly Archive
```bash
# Run Sundays at 2 AM
0 2 * * 0 /path/to/archive.sh
```
