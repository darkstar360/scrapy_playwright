"""This module contains the ``PlaywrightRequest`` class"""

from scrapy import Request


class PlaywrightRequest(Request):
    """Scrapy ``Request`` subclass providing additional arguments"""

    def __init__(self, browser=None, timeout=None, user_agent=None, wait_until=None, screenshot=False, script=None,
                 *args,
                 **kwargs):
        """Initialize a new playwright request

        """

        self.timeout = timeout
        self.wait_until = wait_until  # does not do anything yet
        self.screenshot = screenshot  # does not do anything yet
        self.script = script  # does not do anything yet
        self.browser = browser  # pass browser to the playwright
        self.user_agent = user_agent  # pass user-agent to the playwright

        super().__init__(*args, **kwargs)
