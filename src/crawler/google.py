from playwright.async_api import async_playwright
import aiohttp
import asyncio

from downloader import ImageDownloader


class GoogleCrawler:

    def __init__(self,
                 keyword,
                 save_folder,
                 limit=100):

        self.keyword = keyword

        self.limit = limit

        self.downloader = ImageDownloader(save_folder)

    async def crawl(self):

        async with async_playwright() as p:

            browser = await p.chromium.launch(
                headless=True
            )

            page = await browser.new_page()

            await page.goto(
                "https://www.google.com/imghp"
            )

            await page.fill(
                "textarea",
                self.keyword
            )

            await page.keyboard.press("Enter")

            await page.wait_for_timeout(3000)

            collected = set()

            async with aiohttp.ClientSession() as session:

                while len(collected) < self.limit:

                    thumbs = await page.locator("img").all()

                    for img in thumbs:

                        try:

                            await img.click(timeout=1000)

                            await page.wait_for_timeout(500)

                            images = await page.locator(
                                "img[src^='http']"
                            ).all()

                            for full in images:

                                src = await full.get_attribute("src")

                                if src is None:
                                    continue

                                if src.startswith("http"):

                                    if src not in collected:

                                        collected.add(src)

                                        asyncio.create_task(
                                            self.downloader.download(
                                                session,
                                                src
                                            )
                                        )

                        except:
                            pass

                    await page.mouse.wheel(0, 8000)

                    await page.wait_for_timeout(2000)

            await browser.close()
