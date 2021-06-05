import asyncio
import os
from pyppeteer import launch


dirname = os.path.dirname(__file__)
tfd_html = os.path.join(dirname, 'tfd.html')
blackbox_html = os.path.join(dirname, 'blackbox.html')


class Tongdun(object):

    async def async_get_session_id(self):
        browser = await launch(headless=True,
                               handleSIGINT=False,
                               handleSIGTERM=False,
                               handleSIGHUP=False)
        page = await browser.newPage()
        await page.goto(f'file://{tfd_html}', {'waitUntil': 'networkidle2'})
        session_id = await page.evaluate('''() => sessionId''')
        await browser.close()
        return session_id

    async def async_get_blackbox(self):
        browser = await launch(headless=True,
                               handleSIGINT=False,
                               handleSIGTERM=False,
                               handleSIGHUP=False)
        page = await browser.newPage()
        await page.goto(f'file://{blackbox_html}', {'waitUntil': 'networkidle2'})
        blackbox = await page.evaluate('''() => blackbox''')
        await browser.close()
        return blackbox

    def get_session_id(self):
        loop = asyncio.get_event_loop()
        if loop is None:
            loop = asyncio.new_event_loop()
        session_id = loop.run_until_complete(self.async_get_session_id())
        return session_id

    def get_blackbox(self):
        loop = asyncio.get_event_loop()
        if loop is None:
            loop = asyncio.new_event_loop()
        blackbox = loop.run_until_complete(self.async_get_blackbox())
        return blackbox
