# Decision Log

## 2026-02-20: Model Switch from Claude to Kimi

**Context:**
- Claude API key errors: "No API key found for provider 'anthropic'"
- Multiple failed sessions
- Gateway reinstall needed

**Decision:**
Switch primary model from `anthropic/claude-opus-4-6` to `kimi-coding/k2p5`

**Rationale:**
1. Kimi K2.5 has 262k context window (sufficient)
2. No API key issues with Kimi
3. Faster response times
4. Reliable connection

**Impact:**
- All future sessions use Kimi K2.5
- Lower cost (if applicable)
- Better stability

**Status:** ✅ Implemented and working

---

## 2026-02-20: GitHub Infrastructure Setup

**Context:**
User requested:
- Connect to GitHub repository
- Store memory and session logs
- Set up context limit management
- Search for OpenClaw best practices

**Decision:**
Create comprehensive infrastructure in `clawdbot-kimi-agent` repo:
1. Memory organization system
2. Session logging structure
3. Backup and cleanup scripts
4. Documentation

**Rationale:**
- Persistence across sessions
- Better organization
- Automated maintenance
- Knowledge sharing

**Components:**
- `/memory/` - Facts, decisions, projects
- `/sessions/` - Logs and transcripts
- `/scripts/` - Backup and cleanup
- `/docs/` - Setup guides

**Status:** ✅ Implemented

---

## 2026-02-19: 11880.com Scraping Strategy

**Context:**
- Goal: Extract emails from 11880.com (German business directory)
- Automated scraping blocked by Cloudflare
- MacBook can't handle Playwright browsers

**Decision:**
Use JavaScript bookmarklet for manual extraction

**Rationale:**
1. Cloudflare blocks automated requests
2. MacBook RAM insufficient for multiple browsers
3. Hover technique reveals emails without clicking
4. Bookmarklet extracts all emails from page in 1 second

**Workflow:**
1. Open 11880.com page
2. Hover over "Kontakt aufnehmen" buttons
3. Click bookmarklet
4. Copy emails to file
5. Click "Next page"
6. Repeat for 9,122 pages

**Data Collected:**
- 269,699 businesses total
- 27,617 emails (10.2% coverage)
- Sources: Gelbe Seiten + OSM

**Status:** ⏸️ Pending execution

**Alternatives Considered:**
- VPS huren ($20) - Deferred
- Data kopen (€200-500) - Deferred
- Automated scraping - Failed multiple times

---

## 2026-02-19: Channel Setup Priority

**Decision:**
Set up WhatsApp first, then Telegram

**Rationale:**
- WhatsApp already had phone number
- Telegram requires bot creation
- Both needed for redundancy

**Status:** ✅ Both active

---

*Log format: Date | Context | Decision | Rationale | Status*
