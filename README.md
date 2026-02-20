# Telegram Topic Database on GitHub Pages

A web application that automatically fetches and displays messages from a Telegram topic, with enriched YouTube metadata, deployed on GitHub Pages.

## Setup Instructions

### 1. Repository Setup

```bash
# Clone or reinitialize your repository
git clone https://github.com/naz947/cook.git
cd cook
```

### 2. Add GitHub Secrets

Your Telegram API credentials need to be stored as GitHub Secrets (not in .env file):

1. Go to your repository: `https://github.com/naz947/cook`
2. Settings → Secrets and variables → Actions
3. Add these secrets:
   - `TELEGRAM_API_ID` - Your Telegram API ID (get from https://my.telegram.org/apps)
   - `TELEGRAM_API_HASH` - Your Telegram API Hash (get from https://my.telegram.org/apps)
   - `GROUP_ID` - Your Telegram group/supergroup ID where the topic exists

**How to get your Telegram API credentials:**
1. Visit https://my.telegram.org/apps
2. Create an app or use existing one
3. Copy API ID and API Hash
4. Find your group ID by getting info about the group with Telegram client

### 3. First Manual Run

Trigger the workflow manually to test everything:

1. Go to `Actions` tab in your repo
2. Select "Update Telegram Topic Data"
3. Click "Run workflow"
4. Check the logs to verify it works

### 4. Enable GitHub Pages

1. Go to Settings → Pages
2. Set source to **Deploy from a branch**
3. Select branch: `main` (or your default branch)
4. Select folder: `/ (root)`
5. Click Save

Your site will be available at `https://naz947.github.io/cook/`

### 5. File Structure

```
.
├── .github/
│   └── workflows/
│       └── update-data.yml        # GitHub Actions workflow
├── .gitignore                    # Git ignore rules
├── .env.example                  # Example environment file (reference only)
├── requirements.txt              # Python dependencies
├── index.html                    # Frontend (served by GitHub Pages)
├── data_enriched.json            # Auto-updated data (from Telegram)
├── export_topic.py               # Exports messages from Telegram topic
└── enrich_youtube.py             # Enriches data with YouTube metadata
```

## How It Works

1. **GitHub Actions Scheduler**: Runs `update-data.yml` workflow every hour
2. **Data Export**: `export_topic.py` fetches new messages from your Telegram topic
3. **Enrichment**: `enrich_youtube.py` extracts and enriches YouTube links with metadata
4. **Auto-commit**: Updated `data_enriched.json` is committed back to the repository
5. **GitHub Pages**: Serves `index.html` which loads and displays `data_enriched.json`

## Customization

### Change Update Frequency

Edit `.github/workflows/update-data.yml` line with `cron:`:

```yaml
# Every 15 minutes
- cron: '*/15 * * * *'

# Every 30 minutes  
- cron: '*/30 * * * *'

# Twice daily (8 AM and 8 PM UTC)
- cron: '0 8,20 * * *'
```

[Cron syntax guide](https://crontab.guru/)

### Modify Topic ID

Edit `export_topic.py` line `topic_id = 5`:

```python
topic_id = YOUR_TOPIC_ID  # Change this number
```

## Troubleshooting

### Workflow fails with authentication error
- Verify all three secrets are added correctly
- Check credentials at https://my.telegram.org/apps
- Ensure GROUP_ID is correct (use Telegram desktop app to find it)

### No changes committed
- Check the Actions tab logs for errors
- Verify `data_enriched.json` exists in the repository
- Ensure you have write permissions on the repo

### GitHub Pages not showing
- Enable Pages in Settings (see step 4 above)
- Wait 1-2 minutes for first deployment
- Check the Pages deployment status in Settings → Pages

## Local Testing

To test locally before deploying:

```bash
# Create .env file with your credentials (never commit this)
cp .env.example .env
# Edit .env with real values

# Install dependencies
pip install -r requirements.txt

# Run export script
python export_topic.py

# Run enrichment script
python enrich_youtube.py

# Check data_enriched.json
cat data_enriched.json
```

## Security Notes

- ✅ Credentials stored as GitHub Secrets (hidden from logs)
- ✅ `.env` file never committed (in .gitignore)
- ✅ `.session` files ignored (Telegram session data)
- ⚠️ Never put API credentials in code or commit them

## Support

For issues with:
- **Telegram API**: https://core.telegram.org/
- **GitHub Actions**: https://docs.github.com/en/actions
- **This project**: Check workflow logs in Actions tab
