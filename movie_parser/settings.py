BOT_NAME = 'movie_parser'

SPIDER_MODULES = ['movie_parser.spiders']
NEWSPIDER_MODULE = 'movie_parser.spiders'

FEEDS = {
    'movies.csv': {
        'format': 'csv',
        'encoding': 'utf-8',
        'overwrite': True,
    }
}

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

DOWNLOAD_DELAY = 1

ROBOTSTXT_OBEY = False

COOKIES_ENABLED = True
RETRY_ENABLED = True
RETRY_TIMES = 3

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

CONCURRENT_REQUESTS = 2


import logging
logging.getLogger('scrapy_user_agents.user_agent_picker').setLevel(logging.ERROR)

LOG_LEVEL = 'INFO' 

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.0
AUTOTHROTTLE_MAX_DELAY = 10.0