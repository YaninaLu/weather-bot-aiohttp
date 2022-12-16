import asyncio
import aiohttp


class WebScraper:
    def __init__(self, urls):
        self.urls = urls
        self.data_per_page = {}
        asyncio.run(self.scrape())

    @staticmethod
    async def get_data(session, url):
        try:
            async with session.get(url) as response:
                data = await response.text()
                return url, data
        except Exception as err:
            return f"Something went wrong: {err}"

    async def scrape(self):
        routines = []
        async with aiohttp.ClientSession() as session:
            for url in self.urls:
                routines.append(self.get_data(session, url))
            pages_data = await asyncio.gather(*routines)
            for page in pages_data:
                if page:
                    self.data_per_page[page[0]] = page[1]
