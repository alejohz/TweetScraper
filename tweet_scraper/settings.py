from shutil import which
import os


# !!! # Crawl responsibly by identifying yourself (and your website/e-mail) on the user-agent
USER_AGENT = 'Human-Agent'

# settings for spiders
BOT_NAME = 'tweet_scraper'
LOG_LEVEL = 'INFO'

SPIDER_MODULES = ['tweet_scraper.spiders']
NEWSPIDER_MODULE = 'tweet_scraper.spiders'
ITEM_PIPELINES = {
    'tweet_scraper.pipelines.SaveToFilePipeline': 100,
}

# settings for where to save data on disk
SAVE_TWEET_PATH = os.getenv('SAVE_TWEET_PATH')
SAVE_USER_PATH = os.getenv('SAVE_USER_PATH')

DOWNLOAD_DELAY = 1.5
# CLOSESPIDER_ITEMCOUNT = 10000
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'

# settings for selenium
SELENIUM_DRIVER_NAME = 'firefox'
SELENIUM_BROWSER_EXECUTABLE_PATH = which('firefox')
SELENIUM_DRIVER_EXECUTABLE_PATH = which('geckodriver')
SELENIUM_DRIVER_ARGUMENTS = ['-headless', '--window-size=1920,1080',
                             '--no-sandbox', '--disable-gpu']  # '--headless' if using chrome instead of firefox
DOWNLOADER_MIDDLEWARES = {
    'tweet_scraper.middlewares.SeleniumMiddleware': 800
}

ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
