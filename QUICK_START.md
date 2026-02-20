# Quick Start Guide ⚡

Deploy your Telegram Topic Database to GitHub Pages in 5 minutes!

## Step 1: Prepare Your Telegram Credentials (3 minutes)

1. Visit https://my.telegram.org/apps
2. Login with your phone number
3. Create a new app or use existing one
4. Copy these two values:
   - **API ID** (a number, e.g., 12345678)
   - **API Hash** (a string, e.g., abcdef1234567890...)
5. Open your Telegram group/supergroup
6. Find your **GROUP ID** (you may need Telegram CLI or other tool)
7. Know your **Topic ID** (the topic number in your group)

Keep these values handy!

## Step 2: Push to GitHub (2 minutes)

```bash
# Navigate to your project
cd /home/nazeer/projects/cooking/src/cook

# View what will be committed
git status

# Stage all changes
git add .

# Commit
git commit -m "Setup GitHub Pages deployment"

# Push to GitHub
git push origin main
```

✅ All your code is now on GitHub!

## Step 3: Add GitHub Secrets (1 minute)

1. Go to: https://github.com/naz947/cook
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these three secrets:
   
   **Secret 1:**
   - Name: `TELEGRAM_API_ID`
   - Value: Your API ID number (e.g., 12345678)
   
   **Secret 2:**
   - Name: `TELEGRAM_API_HASH`
   - Value: Your API Hash (e.g., abcdef1234567890...)
   
   **Secret 3:**
   - Name: `GROUP_ID`
   - Value: Your group ID (e.g., -1001234567890)

✅ Your credentials are now secure in GitHub!

## Step 4: Enable GitHub Pages (1 minute)

1. Still in Settings, scroll down to **Pages** section
2. Under "Source", select **Deploy from a branch**
3. Select **Branch**: main
4. Select **Folder**: / (root)
5. Click **Save**

You'll see: "Your site is live at https://naz947.github.io/cook/"

✅ GitHub Pages is now active!

## Step 5: Test It! (Instant)

1. Go to: https://github.com/naz947/cook/actions
2. Click: **Update Telegram Topic Data**
3. Click: **Run workflow**
4. Wait ~1 minute for the run to complete
5. Check the logs for any errors
6. Visit: https://naz947.github.io/cook/

✅ Your site should now display your Telegram messages!

---

## Complete! 🎉

Your deployment is live and will automatically update every hour. New messages in your Telegram topic will appear on the website within 1 hour.

### What Happens Now

- **Every hour** (at :00 minute): Workflow runs automatically
- **Data flows**:
  1. Fetches latest messages from your Telegram topic
  2. Enriches YouTube links with metadata & thumbnails
  3. Updates the website
  4. Commits changes to GitHub

### Customization

**Want different update frequency?**
Edit `.github/workflows/update-data.yml`, find line with `cron: '0 * * * *'`:
- `*/15 * * * *` = Every 15 minutes
- `0 */6 * * *` = Every 6 hours
- `0 9 * * *` = Daily at 9 AM UTC

**Want to change your topic?**
Edit `export_topic.py`, change `topic_id = 5` to your topic number

### Troubleshooting

| Problem | Solution |
|---------|----------|
| Workflow fails | Check Actions logs, verify secrets are correct |
| No data showing | Run workflow manually, check data_enriched.json was created |
| GitHub Pages error | Wait 5 mins, clear browser cache, check Pages settings |
| Secrets not working | Verify exact names: TELEGRAM_API_ID, TELEGRAM_API_HASH, GROUP_ID |

### Files You Need to Know

- **`.github/workflows/update-data.yml`** - The automation (runs every hour)
- **`export_topic.py`** - Fetches from Telegram
- **`enrich_youtube.py`** - Adds YouTube metadata
- **`index.html`** - Your web interface
- **`data_enriched.json`** - Your data (auto-updated)

### Need Help?

1. Check [README.md](README.md) for detailed setup
2. See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for step-by-step guide
3. Review [ARCHITECTURE.md](ARCHITECTURE.md) for how it works
4. Check GitHub Actions logs for specific errors

---

## Your Site is Ready! 📊

Visit: **https://naz947.github.io/cook/**

Updates automatically every hour. Enjoy! 🍳
