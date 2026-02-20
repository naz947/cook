import json
import re
import base64
import httpx
from bs4 import BeautifulSoup
import subprocess
import sys

YOUTUBE_REGEX = re.compile(
    r"(https?://(?:www\.)?(?:youtube\.com/(?:watch\?v=|shorts/)|youtu\.be/)([\w\-]+))"
)

HASHTAG_REGEX = re.compile(r"#\w+")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def extract_video_id(url):
    match = YOUTUBE_REGEX.search(url)
    if match:
        return match.group(2)
    return None

def get_youtube_metadata(url, video_id):
    # Try using yt-dlp for reliable metadata extraction
    try:
        result = subprocess.run(
            ["yt-dlp", "-j", "--no-warnings", "--socket-timeout", "10", url],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0:
            try:
                info = json.loads(result.stdout)
                title = info.get("title")
                description = info.get("description", "")[:200]  # Truncate long descriptions
                if title:
                    return title, description
            except json.JSONDecodeError:
                pass
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    except Exception as e:
        pass

    # Fallback: Parse HTML metadata
    try:
        with httpx.Client(timeout=10, follow_redirects=True, headers=HEADERS) as client:
            r = client.get(url)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")

            # Try to find title
            title = None
            
            # Try og:title first (most reliable)
            title_tag = soup.find("meta", attrs={"property": "og:title"})
            if title_tag and title_tag.get("content"):
                title = title_tag["content"].strip()
            
            # Fallback to regular title
            if not title:
                title_tag = soup.find("title")
                if title_tag:
                    title = title_tag.text.replace(" - YouTube", "").strip()

            # Try to find description
            description = ""
            desc_tag = soup.find("meta", attrs={"property": "og:description"})
            if desc_tag and desc_tag.get("content"):
                description = desc_tag["content"].strip()[:200]
            else:
                desc_tag = soup.find("meta", attrs={"name": "description"})
                if desc_tag and desc_tag.get("content"):
                    description = desc_tag["content"].strip()[:200]

            if title:
                return title, description
                
    except Exception:
        pass

    return None, None

def get_thumbnail_base64(video_id):
    """Fetch and encode YouTube thumbnail as base64"""
    thumb_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    
    try:
        with httpx.Client(timeout=10) as client:
            r = client.get(thumb_url)
            if r.status_code == 200:
                return base64.b64encode(r.content).decode("utf-8")
    except Exception:
        # Silently fail - thumbnail is optional
        pass
    
    return None

def main():
    try:
        # Read the exported data
        if not os.path.exists("data.json"):
            print("❌ Error: data.json not found. Run export_topic.py first.")
            sys.exit(1)
        
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        print(f"📝 Enriching {len(data)} items with YouTube metadata...")
        
        for idx, item in enumerate(data, 1):
            text = item.get("text", "")
            
            # Extract hashtags
            item["hashtags"] = HASHTAG_REGEX.findall(text)
            
            item["youtube_title"] = None
            item["youtube_description"] = None
            item["youtube_thumbnail_base64"] = None
            
            # Process YouTube URLs
            for url in item.get("urls", []):
                video_id = extract_video_id(url)
                if video_id:
                    print(f"  [{idx}/{len(data)}] Processing: {video_id}")
                    title, description = get_youtube_metadata(url, video_id)
                    thumbnail_b64 = get_thumbnail_base64(video_id)
                    
                    item["youtube_title"] = title
                    item["youtube_description"] = description
                    item["youtube_thumbnail_base64"] = thumbnail_b64
                    break
        
        with open("data_enriched.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Enriched data saved to data_enriched.json")
        
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing data.json: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import os
    main()