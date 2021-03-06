# -*- coding: utf-8 -*-

# Scrapy settings for jiayuan project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
BOT_NAME = 'jiayuan_aaa'

SPIDER_MODULES = ['jiayuan.spiders']
NEWSPIDER_MODULE = 'jiayuan.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jiayuan (+http://www.yourdomain.com)'

# PROXY_IP = [
#         #{"ipaddr":"61.54.121.45:8080"}
#          #{"ipaddr":"183.232.185.140:80"}
#          {"ipaddr":"202.85.213.220:3128"}
# #         {"ipaddr":"183.232.185.140:80"},
# #         {"ipaddr":"14.18.201.35:81"},
# #         {"ipaddr":"36.42.32.107:8080"},
# #         {"ipaddr":"60.12.126.140:8080"}
#         
#     ]


#mysql数据库信息
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'jiayuan'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
MYSQL_PORT = 3306


# Obey robots.txt rules
ROBOTSTXT_OBEY = False


#使用scrapy-redis里面的去重组件.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 使用scrapy-redis里面的调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 允许暂停后,能保存进度
SCHEDULER_PERSIST = True
# 指定排序爬取地址时使用的队列，
# 默认的 按优先级排序(Scrapy默认)，由sorted set实现的一种非FIFO、LIFO方式。
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
# 可选的 按先进先出排序（FIFO）
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'
# 可选的 按后进先出排序（LIFO）
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderStack'
#http://www.0duzhan.com/blog_content?aid=292

# 指定redis主机
REDIE_URL = None
REDIS_HOST='127.0.0.1'
REDIS_PORT=6379


# 指定redis主机
# REDIS_URL = 'redis://192.168.0.104:6379'
# LOG_FILE ='D:\log.txt'
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32



# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16
#爬取间隔
DOWNLOAD_DELAY = 3


# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# 禁用cookie
COOKIES_ENABLED = False


# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'jiayuan.middlewares.JiayuanSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#     'jiayuan.middlewares.JiayuanDownloaderMiddleware': 543,
# }

DOWNLOADER_MIDDLEWARES = {
#     'jiayuan.middlewares.JiayuanDownloaderMiddleware': 300,
#     "jiayuan.middlewares.LocalRetryMiddleware":100,
#     'jiayuan.middlewares.SeleniumMiddleware': 205,
    'jiayuan.retry_mid.Retry_Custom': 201,
    'jiayuan.RandomProxy.ProxyIP': 100,#代理IP与agent合并到一起了
    'jiayuan.RandomUserAgent.UserAgent': 200,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'jiayuan.pipelines.JiayuanPipeline': 300,
#}


ITEM_PIPELINES = {
    #'FirstProject.pipelines.FirstprojectPipeline': 300,
#     'jiayuan.pipelines.JiayuanMysql':300,
    'scrapy_redis.pipelines.RedisPipeline':400,
    
}
COMMANDS_MODULE = 'jiayuan.commands'

#图片存放路径
IMAGES_STORE ='D:\\spiders\\jiayuan'
#待爬网站的用户名与密码
USER_NAME = '这是我的用户名'
PASSWD = '这是我的密码'


#(即 Item Pipeline) 同时处理(每个response的)item的最大值
CONCURRENT_ITEMS = 50

#Scrapy downloader 并发请求(concurrent requests)的最大值。
CONCURRENT_REQUESTS = 32

USER_PROXY_IP = ["186.224.65.249:6006"]
PROXY_IP_FILE="proxy_ip.txt"
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
