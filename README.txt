环境部署
chrome 64以上
webdriver2.35(62到64)
http://chromedriver.storage.googleapis.com/index.html
python 3.4
pymysql
pip(环境变量C:\Python34\Scripts)
pip install scrapy(Unable to find vcvarsall.bat有些可能需要安装visual c++)
pip install selenium
pip install scarpy-redis
pip install pypiwin32-219-cp34-none-win_amd64.whl
pip install beautifulsoup4
pip install resquests

master机器重要配置
bind 127.0.0.1改成bind 0.0.0.0
在spider中注释掉所有的item返回，只提交requests

slave机器重要配置
redis-cli -h 192.168.1.0 -p 6379(测试登录)
spider的settings:
REDIS_URL = 'redis://192.168.1.112:6379'
spider中打开yield item

配置好之后执行master与slave两个爬虫


用了20个docker容器来爬，发现速度是上去了，但是代理IP的使用还得改一改，同时取一个的话会拒绝连接的