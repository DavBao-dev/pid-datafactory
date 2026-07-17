import aiohttp
import aiofiles
from pathlib import Path
import asyncio
import hashlib


class ImageDownloader:

    def __init__(self, save_folder):

        self.save_folder = Path(save_folder)
        self.save_folder.mkdir(parents=True, exist_ok=True)

        self.downloaded = set()

    async def download(self, session, url):

        if url in self.downloaded:
            return

        self.downloaded.add(url)

        try:

            async with session.get(url, timeout=20) as resp:

                if resp.status != 200:
                    return

                content = await resp.read()

                if len(content) < 3000:
                    return

                ext = ".jpg"

                if "png" in resp.headers.get("Content-Type", ""):
                    ext = ".png"

                filename = hashlib.md5(url.encode()).hexdigest() + ext

                async with aiofiles.open(
                    self.save_folder / filename,
                    "wb"
                ) as f:

                    await f.write(content)

                print("Downloaded", filename)

        except Exception:
            pass
