# OpenClaw Configuration - B Invest Setup

## Current Configuration Summary

```json5
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "kimi-coding/k2p5"
      },
      "workspace": "/Users/testen/.openclaw/workspace"
    }
  },
  "channels": {
    "whatsapp": {
      "dmPolicy": "allowlist",
      "selfChatMode": true,
      "allowFrom": ["+447451227496"]
    },
    "telegram": {
      "botToken": "***REDACTED***",
      "dmPolicy": "allowlist",
      "allowFrom": ["7861184420"]
    }
  },
  "integrations": {
    "serpapi": {
      "apiKey": "***REDACTED***",
      "monthlyLimit": 250
    }
  }
}
```

## Best Practices Learned

### 1. Model Selection
- **Kimi K2.5** is more reliable than Claude for this setup
- 262k context window is sufficient for most tasks
- Use `thinking: low` for faster responses

### 2. Context Management
- Monitor context usage with `openclaw status`
- Summarize sessions when approaching 200k tokens
- Use `memory_search` before answering questions

### 3. Channel Security
- Always use `allowlist` policy for DMs
- Add specific user IDs, not open to all
- Use `groupPolicy: allowlist` for groups

### 4. Tool Usage
- Store API keys in `TOOLS.md` (local only)
- Use SerpAPI for Google searches (250/month limit)
- Browser relay needs Chrome extension activation

### 5. Memory Strategy
- Read `SOUL.md`, `USER.md`, `AGENTS.md` at session start
- Update `MEMORY.md` with important decisions
- Keep daily logs in `memory/YYYY-MM-DD.md`

## Recommended Additions

### Heartbeat Configuration
```json5
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "30m",
        "maxIdle": "2h"
      }
    }
  }
}
```

### Session Limits
```json5
{
  "agents": {
    "defaults": {
      "session": {
        "maxContextTokens": 200000,
        "summarizeAt": 180000
      }
    }
  }
}
```

### Cron Jobs
```json5
{
  "cron": {
    "jobs": [
      {
        "name": "daily-backup",
        "schedule": { "kind": "cron", "expr": "0 3 * * *" },
        "payload": { "kind": "systemEvent", "text": "Run backup script" }
      }
    ]
  }
}
```

## Troubleshooting

### Issue: "No API key found for provider"
**Solution:** Run `openclaw agents add main` and configure auth

### Issue: Browser relay not working
**Solution:** 
1. Open Chrome extension
2. Click "Attach Tab"
3. Wait for green badge

### Issue: Context limit reached
**Solution:**
1. Summarize conversation
2. Archive old session
3. Start fresh session

## Security Notes

- Never commit API keys to GitHub
- Use `.gitignore` for sensitive files
- Keep `credentials/` directory restricted (chmod 700)
- Review `allowFrom` lists regularly

## Resources

- Docs: https://docs.openclaw.ai
- FAQ: https://docs.openclaw.ai/faq
- Config Reference: https://docs.openclaw.ai/gateway/configuration-reference
- Community: https://discord.com/invite/clawd
