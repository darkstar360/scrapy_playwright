"""This module contains the ``PlaywrightMiddleware`` scrapy middleware"""

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
        self.proxies_capabilities = proxies_capabilities
        self.headless = headless

    @classmethod
    def from_crawler(cls, crawler):
        headless = crawler.settings.get('HEADLESS')
        proxies_capabilities = crawler.settings.get('PROXIES')
        middleware = cls(
            headless=headless,
            proxies_capabilities=proxies_capabilities,
        )

        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)

        return middleware

    def process_request(self, request, spider):
        """Process a request using the selenium driver if applicable"""
        if request.browser is None:
            p = sync_playwright().start()
            self.browser = p.chromium.launch(headless=self.headless)
        else:
            self.browser = request.browser
        if request.user_agent is None:
            request.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        if self.proxies_capabilities is not None:
            if len(self.proxies_capabilities) > 0:
                proxy = random.choice(self.proxies_capabilities)
                pr = proxy.split('@')
                if len(pr) > 1:
                    proxy_server = pr[0]
                    pr_auth = pr[1].split(':')
                    proxy_user = pr_auth[0]
                    proxy_pass = pr_auth[1]
                    self.driver = self.browser.new_context(viewport={'width': 2640, 'height': 1440},
                                                           user_agent=request.user_agent,
                                                           proxy={'server': proxy_server, 'username': proxy_user,
                                                                  'password': proxy_pass})
                else:
                    proxy_server = pr[0]
                    self.driver = self.browser.new_context(viewport={'width': 2640, 'height': 1440},
                                                           user_agent=request.user_agent,
                                                           proxy={'server': proxy_server})
            else:
                self.driver = self.browser.new_context(viewport={'width': 2640, 'height': 1440},
                                                       user_agent=request.user_agent, )
        else:
            self.driver = self.browser.new_context(viewport={'width': 2640, 'height': 1440},
                                                   user_agent=request.user_agent, )
        self.page = self.driver.new_page()

        if not isinstance(request, PlaywrightRequest):
            return None
        if request.timeout:
            self.page.set_default_timeout(request.timeout)
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
