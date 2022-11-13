# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# extracted data -> temporary -> store at database

import scrapy


class Pazar3Items(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    price = scrapy.Field()
    num_of_rooms = scrapy.Field()
    area = scrapy.Field()
    location = scrapy.Field()
    link = scrapy.Field()


class Reklama5Items(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    num_of_rooms = scrapy.Field()
    area = scrapy.Field()
    location = scrapy.Field()
