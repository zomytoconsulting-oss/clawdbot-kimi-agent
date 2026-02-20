# 🧠 Memory Organization Guide

## Core Principles

1. **Write it down** - Don't rely on memory across sessions
2. **Structured storage** - Use consistent formats
3. **Regular cleanup** - Archive old data
4. **Summarize** - Keep only what's needed

## Memory Types

### 1. Facts (`facts/`)
Immutable facts about the user and environment.

```markdown
## User
- **Name:** B Invest
- **Timezone:** Europe/Amsterdam
- **Language:** Dutch/English

## Tools
- SerpAPI: 250 searches/month
- Kimi K2.5: Primary model
- Browser Relay: Chrome extension

## Preferences
- No half-work: "geen halve werk doen"
- Direct communication
- Results-focused
```

### 2. Decisions (`decisions/`)
Important decisions with context and rationale.

```markdown
## 2026-02-20: Model Choice
**Decision:** Use Kimi K2.5 instead of Claude
**Rationale:** Claude API key issues, Kimi more reliable
**Impact:** All future sessions use Kimi
```

### 3. Projects (`projects/`)
Active and completed projects.

```markdown
## 11880.com Scraper
**Status:** In Progress
**Started:** 2026-02-19
**Goal:** Extract emails from German business directory
**Progress:** 269,699 businesses collected
**Blocker:** MacBook can't handle automated scraping
**Solution:** Bookmarklet for manual extraction
```

## Context Management

### When to Summarize
- Session > 200k tokens
- Project completed
- Decision made
- Daily at session end

### Summary Template
```markdown
## Session Summary - YYYY-MM-DD
### Key Events
- Event 1
- Event 2

### Decisions Made
- Decision 1

### Action Items
- [ ] Task 1
- [ ] Task 2

### Files Created/Modified
- path/to/file
```

## Search Strategy

Use `memory_search` before answering:
1. Search for relevant keywords
2. Read matching files
3. Include source citations
4. Update if information changed
