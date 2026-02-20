# 🤖 B Invest - OpenClaw Agent Infrastructure

## 📁 Repository Structure

```
clawdbot-kimi-agent/
├── memory/                 # Long-term memory storage
│   ├── README.md          # Memory organization guide
│   ├── facts/             # Facts and knowledge
│   ├── decisions/         # Decision logs
│   └── projects/          # Project-specific memories
├── sessions/              # Session logs and transcripts
│   ├── logs/              # Daily session logs
│   └── transcripts/       # Conversation transcripts
├── docs/                  # Documentation
│   ├── setup/             # Setup guides
│   ├── tips/              # Tips and tricks
│   └── troubleshooting/   # Common issues
├── scripts/               # Utility scripts
│   ├── backup.sh          # Backup script
│   └── cleanup.sh         # Cleanup old logs
├── config/                # Configuration examples
│   ├── openclaw.json.example
│   └── channels/          # Channel configs
└── README.md              # This file
```

## 🧠 Memory Management

### Context Limit Strategy
- **Max tokens:** 262k (Kimi K2.5)
- **Warning at:** 200k tokens (80%)
- **Critical at:** 240k tokens (90%)
- **Action:** Summarize and archive when >200k

### Memory Files
| File | Purpose | Update Frequency |
|------|---------|------------------|
| `facts/core.md` | Core facts about user | Per session |
| `facts/tools.md` | Tool configurations | When changed |
| `decisions/log.md` | Important decisions | As needed |
| `projects/active.md` | Active projects | Daily |

## 📊 Session Logging

### Log Format
```
sessions/YYYY-MM-DD/
├── HH-MM-SS-session-key.jsonl
├── summary.md
└── stats.json
```

### Retention Policy
- Keep last 30 days in full
- Archive older sessions monthly
- Keep summaries indefinitely

## 🔌 Channel Configuration

### Active Channels
| Channel | Status | ID |
|---------|--------|-----|
| Telegram | ✅ Active | 7861184420 |
| WhatsApp | ✅ Active | +447451227496 |
| WebChat | ✅ Active | localhost |

### API Keys (Stored Securely)
- **SerpAPI:** 250 searches/month
- **Kimi K2.5:** Primary model

## 🚀 Quick Commands

```bash
# Backup everything
./scripts/backup.sh

# Check session size
openclaw status

# Clean old logs
./scripts/cleanup.sh --days 30
```

## 📈 Projects

### Active
1. **11880.com Scraper** - Email extraction from German business directory
   - Status: Bookmarklet ready, need manual execution
   - Data collected: 269,699 businesses (27,617 emails)

### Backlog
- VPS setup for automated scraping
- Data enrichment pipeline
- Cold email automation

---
*Last updated: 2026-02-20*
*Agent: B Invest*
