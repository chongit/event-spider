# Scrapy settings for horse17 project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'horse17'

SPIDER_MODULES = ['horse17.spiders']
NEWSPIDER_MODULE = 'horse17.spiders'

ITEM_PIPELINES = {
    'horse17.pipelines.ReplaceInvalidCharaterPipeline':100,
    'horse17.pipelines.MysqlStorePipeline':200
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'horse17 (+http://www.yourdomain.com)'
