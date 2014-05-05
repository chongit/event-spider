# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Horse17Item(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    source_url = Field()
    logo = Field()
    performer = Field()
    organizer = Field()
    organizerlink = Field()
    starttime = Field()
    endtime = Field()
    description = Field()
    city = Field()
    district = Field()
    address = Field()
    image = Field()
    tags = Field()
    tel = Field()
    email = Field()
    qq = Field()
    weichat = Field()
    loop = Field()
    groups = Field()
    hot = Field()
