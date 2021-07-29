**scrapy playwright**\
**Scrapy Middleware for playwright**\
**Installation**\
`pip install git+https://github.com/darkstar360/scrapy_playwright`

**Features**\
✔fast playwright chromium\
✔ supports proxy and proxy rotation\
for proxy add `PROXIES = ['127.0.0.1:8080@user:pass']`. Add `PROXIES` parameter in the scrapy `settings.py`.<br>
The `PROXIES` parameter takes a python `list`.\
The middleware will choose the proxy randomly if there are more than one proxy is available.

TODO:\
✨Rotating user agents<br> ✨Allowing other browsers