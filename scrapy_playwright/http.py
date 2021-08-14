"""This module contains the ``PlaywrightRequest`` class"""

from scrapy import Request


class PlaywrightRequest(Request):
    """Scrapy ``Request`` subclass providing additional arguments"""

    def __init__(self, browser=None, timeout=None, user_agent=None, wait_until=None, screenshot=False, script=None,
                 *args,
                 **kwargs):
        """Initialize a new selenium request

        Parameters
        ----------
        wait_time: int
            The number of seconds to wait.
        wait_until: method
            One of the "selenium.webdriver.support.expected_conditions". The response
            will be returned until the given condition is fulfilled.
        screenshot: bool
            If True, a screenshot of the page will be taken and the data of the screenshot
            will be returned in the response "meta" attribute.
        script: str
            JavaScript code to execute.

        """

        self.timeout = timeout
        self.wait_until = wait_until
        self.screenshot = screenshot
        self.script = script
        self.browser = browser
        self.user_agent = user_agent

        super().__init__(*args, **kwargs)
