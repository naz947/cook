# Architecture & Workflow

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    TELEGRAM TOPIC                                │
│              (Your cooking links & messages)                     │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ (API Access with credentials)
             │
┌────────────▼────────────────────────────────────────────────────┐
│          GITHUB ACTIONS (Runs Every Hour)                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 1. export_topic.py                                       │   │
│  │    - Connects to Telegram API                            │   │
│  │    - Fetches all messages from topic                    │   │
│  │    - Saves to data.json                                │   │
│  └──────────────────────────────┬───────────────────────────┘   │
│                                 │                                │
│  ┌──────────────────────────────▼───────────────────────────┐   │
│  │ 2. enrich_youtube.py                                     │   │
│  │    - Reads data.json                                    │   │
│  │    - Extracts YouTube links                            │   │
│  │    - Fetches titles, descriptions, thumbnails         │   │
│  │    - Extracts hashtags                                │   │
│  │    - Saves to data_enriched.json                       │   │
│  └──────────────────────────────┬───────────────────────────┘   │
│                                 │                                │
│  ┌──────────────────────────────▼───────────────────────────┐   │
│  │ 3. Git Commit & Push                                     │   │
│  │    - Commits data_enriched.json to GitHub              │   │
│  │    - Pushes changes to main branch                     │   │
│  └──────────────────────────────┬───────────────────────────┘   │
└────────────────────────────────┬───────────────────────────────┘
                                 │
                                 │
┌────────────────────────────────▼───────────────────────────────┐
│          GITHUB REPOSITORY                                      │
│  (Main branch with updated data_enriched.json)                 │
└────────────────────────────────┬───────────────────────────────┘
                                 │
                                 │
┌────────────────────────────────▼───────────────────────────────┐
│          GITHUB PAGES (Static Hosting)                          │
│  Serves index.html + data_enriched.json                        │
└────────────────────────────────┬───────────────────────────────┘
                                 │
                                 │
┌────────────────────────────────▼───────────────────────────────┐
│        WEB BROWSER (Your Users)                                 │
│  https://naz947.github.io/cook/                               │
│                                                                │
│  - Loads index.html                                           │
│  - Fetches data_enriched.json                                │
│  - Displays cards with:                                       │
│    * YouTube titles                                          │
│    * Descriptions                                            │
│    * Thumbnails                                              │
│    * Hashtags                                                │
│    * Search functionality                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Timeline

```
Time: 00:00 UTC
├─ GitHub Actions trigger (hourly)
│  ├─ Checkout repository
│  ├─ Install Python + dependencies
│  ├─ Run: python export_topic.py
│  │  └─ Fetch messages from Telegram topic → data.json
│  ├─ Run: python enrich_youtube.py
│  │  └─ Enrich with metadata → data_enriched.json
│  ├─ Git commit (if changes detected)
│  └─ Git push to main branch
│
└─ GitHub Pages detects update
   ├─ Rebuild & redeploy
   └─ Serves new content within 1-2 seconds

Time: 01:00 UTC → Repeat
```

## Key Features

### ✅ Fully Automated
- Runs every hour without manual intervention
- Detects and commits only when data changes
- Handles errors gracefully (continues if one step fails)

### ✅ GitHub Secrets Protection
- API credentials stored in GitHub Secrets
- Never visible in logs or code
- Automatically injected at runtime

### ✅ Efficient Updates
- Only commits when data actually changes
- Saves bandwidth and git history
- Graceful handling of network failures

### ✅ Rich Data Enrichment
- YouTube video titles & descriptions
- Thumbnail images (base64 encoded)
- Hashtag extraction
- Full-text search in web interface

### ✅ No Server Required
- Runs on GitHub's free infrastructure
- Static hosting via GitHub Pages
- Zero monthly cost

## Environment Variables

Your GitHub Actions workflow injects these from Secrets:

```yaml
TELEGRAM_API_ID=12345678        # Your Telegram API ID (number)
TELEGRAM_API_HASH=abc123...     # Your Telegram API Hash (string)
GROUP_ID=9087654321             # Your group ID where topic exists
```

## Storage

- **GitHub Repository**: Single source of truth
  - `data.json` - Raw Telegram messages
  - `data_enriched.json` - Enriched version (served to users)
  - Git history tracks all changes

- **GitHub Pages**: Static files served from main branch
  - `index.html` - Web interface
  - `data_enriched.json` - Latest data

- **GitHub Actions**: Workflow logs stored for 90 days
  - Useful for debugging if something goes wrong

## Execution Requirements

- **Timezone**: All scheduled runs use UTC
- **Frequency**: Configurable (default: hourly)
- **Duration**: ~2-5 minutes per run (depending on message count)
- **Quota**: Free tier includes 2,000 min/month (plenty for hourly)

## File Operations

```
import → python files
├─ export_topic.py reads:
│  └─ Credentials from environment (TELEGRAM_*)
│
├─ enrich_youtube.py reads:
│  ├─ data.json (from export_topic)
│  ├─ YouTube HTML/metadata
│  └─ YouTube thumbnails (HTTP)
│
└─ Both write:
   ├─ data.json → Git tracked
   └─ data_enriched.json → Served via Pages
```

## Security Considerations

✅ **Protected**
- API secrets in GitHub Secrets (not in code)
- Telegram session files in .gitignore
- .env file in .gitignore (for local development)

⚠️ **Exposed**
- Public GitHub repository (visible to everyone)
- Public GitHub Pages site (anyone can access data)
- Git commit history (visible in repository)

## Scalability

Current performance at ~10 messages/hour:
- Export: ~1-2 seconds
- Enrichment: ~2-3 seconds (depends on YouTube API)
- Total: ~3-5 minutes including Git operations

At 100 messages:
- Proportional increase (~0.3-0.5 sec per message enrichment)
- May hit YouTube rate limits (handled gracefully)

## Next Actions

1. **Setup secrets**: Add TELEGRAM_API_ID, TELEGRAM_API_HASH, GROUP_ID
2. **Push to GitHub**: `git push origin main`
3. **Enable Pages**: Settings → Pages → Deploy from branch
4. **Test manually**: Actions → Run workflow
5. **Verify**: Check https://naz947.github.io/cook/
