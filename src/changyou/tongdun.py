import asyncio
import time
import os
import random
from pyppeteer import launch


dirname = os.path.dirname(__file__)
tfd_html = os.path.join(dirname, 'tfd.html')
blackbox_html = os.path.join(dirname, 'blackbox.html')


class Tongdun(object):

    async def async_get_blackbox(self):
        browser = await launch(headless=True,
                               handleSIGINT=False,
                               handleSIGTERM=False,
                               handleSIGHUP=False,
                               args=['--no-sandbox'])
        page = await browser.newPage()
        await page.goto(f'file://{blackbox_html}', {'waitUntil': 'networkidle2'})
        blackbox = await page.evaluate('''() => blackbox''')
        await browser.close()
        return blackbox

    def get_session_id(self):
        ts = int(time.time() * 1000)
        suffix = random.uniform(0, 1).hex()[4:-3]
        return f'changyo-pc-{ts}-{suffix}'

    def get_blackbox(self):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
        blackbox = loop.run_until_complete(self.async_get_blackbox())
        return blackbox
