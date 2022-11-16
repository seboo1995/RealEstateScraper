import scrapy
from ..items import Reklama5Items
import cyrtranslit
import time
import re


class reklama5Spider(scrapy.Spider):
    reklama_5_base_url = 'https://reklama5.mk'
    name = 'Reklama5Spider'
    custom_settings = {
        'ITEM_PIPELINES': {
            'real_estate_scraper.pipelines.Reklama5Pipeline': 400
        }}
    start_urls = [
        'https://reklama5.mk/Search?city=1&cat=159&q=&f45_from=&f45_to=&f46_from=&f46_to=&priceFrom=&priceTo=&f48_from=&f48_to=&f47=&f10029=&f10030=&f10040=&sell=0&sell=1&buy=0&rent=0&includeforrent=0&trade=0&includeOld=0&includeNew=0&private=0&company=0&page=1']

    def parse(self, response):
        time.sleep(2)
        all_links = response.css('a.SearchAdTitle::attr(href)').extract()
        all_links = [self.reklama_5_base_url+i for i in all_links]
        for link in all_links:
            yield response.follow(link, callback=self.parse_ad)
        next_page = self.reklama_5_base_url + \
            response.css('a.page-link[title]::attr(href)').get()

        match_obj = re.search('page=[0-9]', next_page)
        page_number = int(next_page[match_obj.start()+5:match_obj.end()])

        if page_number <= 10:
            print("NEXT PAGE IS", next_page)
            yield response.follow(next_page, callback=self.parse)

    def parse_ad(self, response):
        items = Reklama5Items()
        title = response.css('h5.card-title::text').extract_first()
        link = response.url
        price = response.css('h5.mb-0::text').extract_first()
        amenities_keys = response.css('.col-5 p::text').extract()
        amenities_values = response.css(
            'div.col-7:nth-of-type(n+2) p::text').extract()
        try:
            num_of_rooms = amenities_values[amenities_keys.index(
                'Број на соби:')]
        except:
            num_of_rooms = 'N/A'
        try:
            area = amenities_values[amenities_keys.index('Квадратура:')]
        except:
            area = 'N/A'

        location = response.css('.align-self-center p::text').extract_first()

        items['title'] = cyrtranslit.to_latin(title)
        items['link'] = link
        items['price'] = price
        items['num_of_rooms'] = num_of_rooms
        items['area'] = area
        items['location'] = cyrtranslit.to_latin(location)

        yield items
