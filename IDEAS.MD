
2. Proxy can now be a generator to pick a random proxy from a file for each task created by asyncio. Note, the generator must be able to yield as long as requests are being created.

Example:

def generator_random_choice(filename):
    with open(filename) as f:
        lines = f.readlines()

    def _generator():
        while True:
            yield random.choice(lines)

    return _generator()

Solved bug regex parser trying to connect with a website where the url contains html code by:
3. We now use lxml to extract all links from a page and than use the Regex from the parser to filter the correct links from the result.

4. Implemented Aiocache so users can use redis, memcache or memory cache to lower throttling and or prevent going back to source when crawler is being re-run while the source data has not changed a bit.

5. Improve Css Selector; There is in the current version not allot of control on what to actually get from the css. And since the selectors are class instances we cannot give the user any control of using the internal libraries to improve result performance.

# Css(sub_method='text_content', expression='div#breadcrumb span', index='6')
# Css(method='text', expression='.deal-page-title', index='0')
# Css(method='text_content', expression='.deal-page-title', index='0')
# Css(method='get', expression='div.map_canvas',index='0', attribute='data-address')
# Css(method='get', expression='meta[property="og:title"]', index='0', attribute='content')
# Css(method='itertext', expression='span.formattedAddress', index='0')
# Css(method='get', expression='div#tabcontentWrapper #tabContent1 a', index='0', attribute='title')
# Css(method='get', expression='div#tabcontentWrapper #tabContent1 a', index='0', attribute='href')
# Css(method='get', expression='div#tabcontentWrapper #tabContent1 img', index='0', attribute='alt')
# Css(method='get', expression='div#tabcontentWrapper #tabContent1 img', index='0', attribute='src', split = '/', splitIndex='-3')

6. Scrape a single document from cache to test your CSS code.

Potential improvements:

Implement much more CSS statement control.
Use LRU cache on lxml related functions in case we find the same URL and can use cache from memory.
Use pyppeteer to scrape client side rendered websites. => https://pypi.org/project/pyppeteer/



# Asios Pro Version

# email check => https://github.com/JoshData/python-email-validator or https://github.com/JoshData/python-email-validator; https://www.scottbrady91.com/Email-Verification/Python-Email-Verification-Script, https://aiosmtpd.readthedocs.io/en/latest/
# info, contact, bezoek
# check if contact page exist from a website and if so extract phone, address, email
# This, so you can furthermore investigate 
# Should we divide cache as an instance object so we can talk to the cache from the async def save?

# Names

Word: data, mining, scraping, analytics, async, io, 

* Asios (Kever geslacht)
* Scrapy -> Scrapio





Remove webserver and go for a fake server implementation:
- https://gist.github.com/webknjaz/7057aa077858a111dd16aefcaa0c7813