# GitHub Pages Deployment Checklist

## Pre-Deployment (Local Setup)

- [ ] Clone repository: `git clone https://github.com/naz947/cook.git && cd cook`
- [ ] Run setup script: `bash setup.sh`
- [ ] Edit `.env` with your Telegram credentials
  - [ ] Get API_ID from https://my.telegram.org/apps
  - [ ] Get API_HASH from https://my.telegram.org/apps
  - [ ] Get GROUP_ID (Telegram group ID with topic)
- [ ] Test locally: `python export_topic.py && python enrich_youtube.py`
- [ ] Verify `data_enriched.json` is created and has content
- [ ] Commit initial files: `git add . && git commit -m "Initial setup"`

## GitHub Setup

- [ ] Push to GitHub: `git push origin main`
- [ ] Verify all files are in repository (including `.gitignore`)
- [ ] Go to repository Settings → Secrets and variables → Actions
- [ ] Add these secrets:
  - [ ] `TELEGRAM_API_ID` = your API ID
  - [ ] `TELEGRAM_API_HASH` = your API Hash
  - [ ] `GROUP_ID` = your group ID

## GitHub Pages Configuration

- [ ] Go to Settings → Pages
- [ ] Set source to: **Deploy from a branch**
- [ ] Select branch: `main` (or default branch)
- [ ] Select folder: `/ (root)`
- [ ] Click Save
- [ ] Wait 1-2 minutes for first deployment

## First Automated Run

- [ ] Go to Actions tab
- [ ] Select "Update Telegram Topic Data" workflow
- [ ] Click "Run workflow"
- [ ] Monitor execution logs
- [ ] Verify `data_enriched.json` was updated
- [ ] Check GitHub Pages site loads at: https://naz947.github.io/cook/

## Verify Automation

- [ ] Check Actions tab for hourly runs
- [ ] Confirm commits are being made automatically
- [ ] Visit GitHub Pages URL to see updated content
- [ ] Post a message to Telegram topic
- [ ] Wait 1 hour for next scheduled run
- [ ] Verify new message appears in web interface

## Troubleshooting Checklist

If workflow fails:
- [ ] Check Actions tab logs for error messages
- [ ] Verify secrets are correctly set (no typos)
- [ ] Confirm TELEGRAM_API_ID is a number, not a string
- [ ] Verify GROUP_ID is correct (get from Telegram desktop)
- [ ] Ensure topic_id in export_topic.py matches your topic

If GitHub Pages doesn't show:
- [ ] Verify Pages is enabled in Settings
- [ ] Check deployment status in Settings → Pages
- [ ] Clear browser cache or check incognito window
- [ ] Verify index.html exists in repository root
- [ ] Check that data_enriched.json is committed

## Maintenance

- [ ] Review Actions runs weekly for any errors
- [ ] Monitor workflow execution time
- [ ] Update yt-dlp dependency monthly: `pip install --upgrade yt-dlp`
- [ ] Monitor GitHub Pages deployment status
