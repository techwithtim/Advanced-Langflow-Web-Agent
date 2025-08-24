import os
import time
import requests
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

load_dotenv()


def poll_snapshot_status(
    snapshot_id: str, max_attempts: int = 60, delay: int = 5
) -> bool:
    api_key = os.getenv("BRIGHTDATA_API_KEY")
    progress_url = f"https://api.brightdata.com/datasets/v3/progress/{snapshot_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    for attempt in range(max_attempts):
        try:
            print(
                f"⏳ Checking snapshot progress... (attempt {attempt + 1}/{max_attempts})"
            )

            response = requests.get(progress_url, headers=headers)
            response.raise_for_status()

            progress_data = response.json()
            status = progress_data.get("status")

            if status == "ready":
                print("✅ Snapshot completed!")
                return True
            elif status == "failed":
                print("❌ Snapshot failed")
                return False
            elif status == "running":
                print("🔄 Still processing...")
                time.sleep(delay)
            else:
                print(f"❓ Unknown status: {status}")
                time.sleep(delay)

        except Exception as e:
            print(f"⚠️ Error checking progress: {e}")
            time.sleep(delay)

    print("⏰ Timeout waiting for snapshot completion")
    return False


def download_snapshot(
    snapshot_id: str, format: str = "json"
) -> Optional[List[Dict[Any, Any]]]:
    api_key = os.getenv("BRIGHTDATA_API_KEY")
    download_url = (
        f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}?format={format}"
    )
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        print("📥 Downloading snapshot data...")

        response = requests.get(download_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        print(
            f"🎉 Successfully downloaded {len(data) if isinstance(data, list) else 1} items"
        )

        return data

    except Exception as e:
        print(f"❌ Error downloading snapshot: {e}")
        return None
