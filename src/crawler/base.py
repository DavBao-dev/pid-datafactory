from playwright.async_api import async_playwright
import asyncio


class BaseCrawler:

    async def start(self):

        self.playwright = await async_playwright().start()

        self.browser = await self.playwright.chromium.launch(
            headless=True
        )

    async def stop(self):

        await self.browser.close()

        await self.playwright.stop()
