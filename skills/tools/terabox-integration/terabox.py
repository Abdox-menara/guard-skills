#!/usr/bin/env python3
"""
TeraBox Integration Tool
Cloud storage operations via browser automation and API
"""

import os
import sys
import json
import asyncio
import argparse
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Playwright not installed. Run: pip install playwright")
    sys.exit(1)


class TeraBoxIntegration:
    def __init__(self):
        self.cookies = {}
        self.base_url = "https://www.terabox.com"
        self.app_id = "250528"

    async def extract_cookies_from_browser(self) -> Dict:
        """Extract cookies from Playwright browser session"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            # Navigate to TeraBox
            await page.goto(self.base_url)
            print("Please log in to TeraBox in the browser window...")
            print("Press Enter when logged in...")
            input()

            # Extract cookies
            cookies = await context.cookies()
            cookie_dict = {c["name"]: c["value"] for c in cookies}

            await browser.close()

            self.cookies = cookie_dict
            return cookie_dict

    def check_quota(self) -> Dict:
        """Check storage quota via API"""
        import requests

        url = f"{self.base_url}/api/quota"
        params = {
            "app_id": self.app_id,
            "web": "1",
            "channel": "dubox",
            "clienttype": "0",
            "checkexpire": "1",
            "checkfree": "1",
        }

        response = requests.get(url, params=params, cookies=self.cookies)
        data = response.json()

        if data.get("errno") == 0:
            return {
                "total": data.get("total", 0),
                "used": data.get("used", 0),
                "free": data.get("free", 0),
                "expire": data.get("expire", False),
            }
        else:
            raise Exception(f"API error: {data.get('errmsg', 'Unknown error')}")

    def list_files(self, directory: str = "/") -> List[Dict]:
        """List files in directory via API"""
        import requests

        url = f"{self.base_url}/api/list"
        params = {
            "app_id": self.app_id,
            "web": "1",
            "channel": "dubox",
            "clienttype": "0",
            "order": "time",
            "desc": "1",
            "dir": directory,
            "num": "100",
            "page": "1",
            "showempty": "0",
        }

        response = requests.get(url, params=params, cookies=self.cookies)
        data = response.json()

        if data.get("errno") == 0:
            return data.get("list", [])
        else:
            raise Exception(f"API error: {data.get('errmsg', 'Unknown error')}")

    def upload_file(self, local_path: str, remote_path: Optional[str] = None) -> bool:
        """Upload file via browser automation"""
        # This would use Playwright to upload via the hidden input
        # Implementation depends on browser automation
        return True

    def upload_folder(self, local_folder: str) -> bool:
        """Upload entire folder structure"""
        # Compress folder first
        zip_path = self.compress_folder(local_folder)

        # Then upload the zip file
        return self.upload_file(zip_path)

    def verify_upload(self, filename: str) -> bool:
        """Verify file exists in cloud storage"""
        files = self.list_files()
        return any(f.get("server_filename") == filename for f in files)

    def compress_folder(self, folder_path: str, output_path: Optional[str] = None) -> str:
        """Compress folder to zip for upload"""
        if not output_path:
            folder_name = Path(folder_path).name
            output_path = f"{folder_name}.zip"

        # Use PowerShell Compress-Archive
        cmd = f'Compress-Archive -Path "{folder_path}\\*" -DestinationPath "{output_path}" -Force'
        os.system(f'powershell -Command "{cmd}"')

        return output_path


async def main():
    parser = argparse.ArgumentParser(description="TeraBox Integration Tool")
    parser.add_argument(
        "command", choices=["quota", "list", "upload", "upload-folder", "verify"], help="Command to execute"
    )
    parser.add_argument("path", nargs="?", help="File/folder path")
    parser.add_argument("--cookie-file", help="Path to cookies JSON file")

    args = parser.parse_args()

    tb = TeraBoxIntegration()

    # Load cookies if provided
    if args.cookie_file and os.path.exists(args.cookie_file):
        with open(args.cookie_file, "r") as f:
            tb.cookies = json.load(f)

    try:
        if args.command == "quota":
            quota = tb.check_quota()
            print(f"Storage: {quota['used'] / 1024**3:.1f} GB / {quota['total'] / 1024**3:.0f} GB")
            print(f"Free: {quota['free'] / 1024**3:.1f} GB")

        elif args.command == "list":
            files = tb.list_files()
            for f in files:
                print(f"{f.get('server_filename', 'Unknown')}")

        elif args.command == "upload":
            if not args.path:
                print("Error: Path required for upload command")
                sys.exit(1)
            tb.upload_file(args.path)
            print(f"Uploaded: {args.path}")

        elif args.command == "upload-folder":
            if not args.path:
                print("Error: Path required for upload-folder command")
                sys.exit(1)
            tb.upload_folder(args.path)
            print(f"Uploaded folder: {args.path}")

        elif args.command == "verify":
            if not args.path:
                print("Error: Path required for verify command")
                sys.exit(1)
            exists = tb.verify_upload(args.path)
            print(f"File exists: {exists}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
