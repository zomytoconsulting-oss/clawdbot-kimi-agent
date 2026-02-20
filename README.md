# 🤖 B Invest - OpenClaw Agent Infrastructure

## 🚀 What's Included

This repository contains a **complete, optimized OpenClaw setup** with:
- ✅ **QMD Memory** - Local-first quantum memory database
- ✅ **Session Pruning** - Automatic context optimization
- ✅ **Memory Flush** - Never lose important data
- ✅ **Multi-channel** - Telegram + WhatsApp + WebChat
- ✅ **Documentation** - Complete setup guides

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
│   ├── OPTIMIZATION.md    # Performance optimization guide
│   ├── QMD-SETUP.md       # QMD installation & setup ⭐ NEW
│   └── setup-guide.md     # General setup guide
├── scripts/               # Utility scripts
│   ├── backup.sh          # Backup script
│   └── cleanup.sh         # Cleanup old logs
├── config/                # Configuration examples
│   ├── openclaw-qmd.json          # Config WITH QMD ⭐
│   ├── openclaw-optimized.json    # Config without QMD
│   └── setup-guide.md             # Setup instructions
└── README.md              # This file
```

## 🧠 Memory Systems

### Option 1: QMD (Quantum Memory Database) ⭐ RECOMMENDED
**Status:** ✅ Installed and configured
**Features:**
- 100% Local embeddings (no external API)
- BM25 + Vector search combined
- Advanced reranking
- Full privacy
- Better performance

**Setup:** See `docs/QMD-SETUP.md`

**Quick Start:**
```bash
cp config/openclaw-qmd.json ~/.openclaw/openclaw.json
openclaw gateway restart
```

### Option 2: Default Memory
**Features:**
- Works immediately
- Remote embeddings
- Simpler setup

**Quick Start:**
```bash
cp config/openclaw-optimized.json ~/.openclaw/openclaw.json
openclaw gateway restart
```

### Context Limit Strategy
- **Max tokens:** 262k (Kimi K2.5)
- **Warning at:** 200k tokens (80%)
- **Critical at:** 240k tokens (90%)
- **Action:** Auto-flush memories when >238k

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

## ⚡ Optimizations Included

### 1. Automatic Memory Flush
Saves important memories BEFORE context compaction. Never lose data!

### 2. Session Pruning (cache-ttl)
- Removes old tool results after 5 min idle
- Keeps only last 3 assistant messages
- Faster responses, lower costs

### 3. Smart Heartbeat
- Checks every 30 minutes
- Reads HEARTBEAT.md for tasks
- Max idle: 2 hours

### 4. QMD Integration
- Local-first memory search
- BM25 + Vector + Reranking
- 100% privacy

**Documentation:** See `docs/OPTIMIZATION.md`

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
