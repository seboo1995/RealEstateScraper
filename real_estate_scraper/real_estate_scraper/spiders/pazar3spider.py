import scrapy
from ..items import Pazar3Items
import cyrtranslit


class Pazar3Spider(scrapy.Spider):
    name = 'Pazar3Spider'
    custom_settings = {
        'ITEM_PIPELINES': {
            'real_estate_scraper.pipelines.Pazar3Pipeline': 400
        }}
    # start_urls = [
    #    'https://www.pazar3.mk/oglasi/zivealista/stanovi/se-prodava/skopje?Page='+str(i) for i in range(1, 10)]
    start_urls = [
        'https://www.pazar3.mk/oglasi/zivealista/stanovi/se-prodava/skopje']

    def parse(self, response):
        items = Pazar3Items()
        ads_info = response.css('div.title')

        for ad in ads_info:
            title = ad.css('h2 a::text').extract_first()
            link = ad.css('h2 a::attr(href)').extract_first()
            price = ad.css('p.list-price::text').extract_first(), 'mk'
            num_of_rooms = ad.css(
                '.title > div:nth-of-type(1)::text').extract_first()
            area = ad.css(
                'div.new:nth-of-type(n+2) .title div:nth-of-type(2)::text').extract_first()
            location = ad.css(
                'a.link-html5:nth-of-type(n+3)::text').extract_first().strip()

            items['title'] = cyrtranslit.to_latin(title, 'mk')
            items['link'] = 'https://www.pazar3.mk/'+link
            try:
                items['price'] = cyrtranslit.to_latin(price, 'mk')
            except:
                items['price'] = 'N/A'

            try:
                items['num_of_rooms'] = cyrtranslit.to_latin(
                    num_of_rooms, 'mk')
            except:
                items['num_of_rooms'] = None

            try:
                items['location'] = cyrtranslit.to_latin(location, 'mk')
            except:
                items['location'] = 'N/A'

            try:
                items['num_of_rooms'] = num_of_rooms
            except:
                items['number_of_rooms'] = None
            try:
                items['area'] = cyrtranslit.to_latin(area, 'mk')
            except:
                items['area'] = None
            yield items
        next_page = response.css(
            'li:nth-of-type(11) a.link-html5::attr(href)').get()
        if '?Page=30' not in next_page:
            print("NEXT PAGE IS", next_page)
            yield response.follow(next_page, callback=self.parse)
