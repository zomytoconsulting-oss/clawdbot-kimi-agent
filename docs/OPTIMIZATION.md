# 🚀 OPTIMIZED CONFIGURATION - B Invest

## Samenvatting van Verbeteringen

Gebaseerd op officiële OpenClaw documentatie (docs.openclaw.ai):

---

## 1. 🧠 AUTOMATISCHE MEMORY FLUSH

**Wat het doet:** Slaat automatisch belangrijke herinneringen op VOORDAT de context wordt gecomprimeerd.

**Config:**
```json5
{
  agents: {
    defaults: {
      compaction: {
        reserveTokensFloor: 20000,
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 4000,
          systemPrompt: "Session nearing compaction. Store durable memories now.",
          prompt: "Write lasting notes to memory/YYYY-MM-DD.md; reply NO_REPLY if nothing to store."
        }
      }
    }
  }
}
```

**Voordelen:**
- ✅ Nooit meer data verlies bij context limit
- ✅ Automatisch archival van belangrijke informatie
- ✅ Stille operatie (geen gebruiker storen)

---

## 2. ✂️ SESSION PRUNING (cache-ttl)

**Wat het doet:** Verwijdert oude tool results automatisch om tokens te besparen.

**Config:**
```json5
{
  agents: {
    defaults: {
      contextPruning: {
        mode: "cache-ttl",
        ttl: "5m",
        keepLastAssistants: 3,
        softTrimRatio: 0.3,
        hardClearRatio: 0.5,
        minPrunableToolChars: 50000,
        softTrim: {
          maxChars: 4000,
          headChars: 1500,
          tailChars: 1500
        },
        hardClear: {
          enabled: true,
          placeholder: "[Old tool result cleared - see memory files]"
        }
      }
    }
  }
}
```

**Hoe het werkt:**
1. Na 5 minuten idle → pruning activeert
2. Houdt alleen laatste 3 assistant berichten
3. Verwijdert oude tool results (>50k chars)
4. Browser snapshots (groot) worden gecleared
5. Cache window reset = goedkoper!

**Voordelen:**
- ⚡ Snellere responses
- 💰 Lagere API kosten
- 🧹 Schoner context window

---

## 3. 💓 HEARTBEAT OPTIMALISATIE

**Config:**
```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        maxIdle: "2h"
      }
    }
  }
}
```

**Wat het doet:**
- Checkt elke 30 minuten voor taken
- Leest HEARTBEAT.md
- Reageert proactief zonder te storen

---

## 4. 🔍 VECTOR MEMORY SEARCH (Optioneel)

**Wat het doet:** Semantic search over je memory files.

**Config:**
```json5
{
  agents: {
    defaults: {
      memorySearch: {
        enabled: true,
        provider: "gemini", // of "openai", "voyage", "local"
        remote: {
          apiKey: "YOUR_API_KEY"
        }
      }
    }
  }
}
```

**Voordelen:**
- 🧠 Vindt relevante info ook met andere woorden
- 🚀 Snellere recall
- 📊 Betere context begrip

---

## 5. 📊 CONTEXT LIMIT STRATEGIE

**Huidige setup:**
- **Max:** 262k tokens (Kimi K2.5)
- **Warning:** 242k (reserve 20k)
- **Flush:** 238k (4k voor warning)
- **Pruning:** Na 5 min idle

**Status levels:**
| Tokens | Status | Actie |
|--------|--------|-------|
| <200k | 🟢 Safe | Normaal |
| 200-238k | 🟡 Monitor | Let op |
| 238-242k | 🟠 Flush | Auto-save memories |
| >242k | 🔴 Critical | Pruning active |

---

## 🔧 HOE TOE TE PASSEN

1. Open: `~/.openclaw/openclaw.json`
2. Voeg de bovenstaande secties toe onder `agents.defaults`
3. Herstart: `openclaw gateway restart`
4. Check: `openclaw status`

---

## 📁 BESTANDEN AANGEMAAKT

- `openclaw-optimized.json` - Volledige optimized config
- `memory/README.md` - Memory organisatie
- `sessions/README.md` - Session logging
- `scripts/backup.sh` - Automatische backup
- `scripts/cleanup.sh` - Oude logs opruimen

---

## ⚡ DIRECTE VOORDELEN

1. **Sneller:** Pruning verwijdert onnodige data
2. **Goedkoper:** Minder tokens = lagere kosten
3. **Slimmer:** Automatische memory management
4. **Betrouwbaarder:** Geen data verlies bij compaction
5. **Proactief:** Heartbeat checkt taken

---

## 🎯 VOLGENDE STAPPEN

1. ✅ Config toepassen (handmatig of via `openclaw config apply`)
2. ✅ Test met lange sessie
3. ✅ Monitor `openclaw status` voor context usage
4. ✅ Gebruik `memory_search` voor snelle recall

---

*Bronnen:*
- https://docs.openclaw.ai/concepts/memory.md
- https://docs.openclaw.ai/concepts/session-pruning.md
- https://docs.openclaw.ai/concepts/compaction.md

*Agent: B Invest*
*Date: 2026-02-20*
