"""This module contains the ``SeleniumMiddleware`` scrapy middleware"""

from importlib import import_module

from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
import random
from .http import PlaywrightRequest
from playwright.sync_api import sync_playwright


class PlaywrightMiddleware:
    """Scrapy middleware handling the requests using selenium"""

    def __init__(self, proxies_capabilities=None, headless=True):
        p = sync_playwright().start()
        self.browser = p.chromium.launch(headless=False)
        self.driver = self.browser.new_context(viewport={'width': 2640, 'height': 1440})
        self.page = self.driver.new_page()

    @classmethod
    def from_crawler(cls, crawler):
        headless = crawler.settings.get('HEADLESS')
        proxies_capabilities = crawler.settings.get('PROXIES')
        middleware = cls(
            headless=headless,
            proxies_capabilities=proxies_capabilities
        )

        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)

        return middleware

    def process_request(self, request, spider):
        """Process a request using the selenium driver if applicable"""

        if not isinstance(request, PlaywrightRequest):
            return None

        self.page.goto(request.url, wait_until="domcontentloaded")
        # self.page.wait_for_load_state("networkidle")

        body = str.encode(self.page.content())

        # Expose the driver via the "meta" attribute
        request.meta.update({'driver': self.driver, 'browser': self.browser, 'page': self.page})

        return HtmlResponse(
            self.page.url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def spider_closed(self):
        """Shutdown the browser when spider is closed"""
        self.browser.close()
