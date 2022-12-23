import re

import scrapy

from scrapysteam.scrapysteam.items import Game

queries = ['term=Minecraft', 'term=Counter+Strike', 'term=Rust']


class SteamgamesspiderSpider(scrapy.Spider):
    name = 'SteamGamesSpider'

    def start_requests(self):
        for query in queries:
            url = 'https://store.steampowered.com/search/?' + query
            yield scrapy.Request(url, callback=self.parse_keyword_response)

    def parse_keyword_response(self, response):
        products = []
        for elem in response.css('a::attr(href)').getall():
            if re.search(r'app', elem):
                products.append(elem)

        for product in products:
            yield scrapy.Request(product, callback=self.parse)

    def parse(self, response):
        item = Game()
        name = response.xpath('//div[@class="apphub_AppName"]/text()')
        if len(name) == 0:
            yield item
        else:
            category = response.xpath('//div[@class="blockbg"]/*/text()')
            rating = response.xpath('//meta[@itemprop = "ratingValue"]/@content')
            if len(rating) > 0:
                rating = rating[0].get()
            else:
                rating = None
            number_of_reviews = response.xpath('//meta[@itemprop = "reviewCount"]/@content')
            if len(number_of_reviews) > 0:
                number_of_reviews = number_of_reviews[0].get()
            else:
                number_of_reviews = None
            release_date = response.xpath('//div[@class="release_date"]/div[@class="date"]/text()')
            if len(release_date) > 0:
                release_date = release_date[0].get()
            else:
                release_date = None
            developer = response.xpath('//div[@class="dev_row"]/div[@class="summary column"]/*/text()')
            tags = response.xpath('//div[@class="glance_tags popular_tags"]/*/text()')
            tags = [s.get().strip() for s in tags]
            price = response.xpath('//div[@class="game_area_purchase_game_wrapper"]//div['
                                   '@class="discount_original_price"]/text()')
            if len(price) == 0:
                price = response.xpath('//div[@class="game_area_purchase_game_wrapper"]//div['
                                       '@class="game_purchase_price price"]/text()')
                if len(price) == 0:
                    price = None
                else:
                    price = re.sub(r'(\d+)(.*)', r'\1', price[0].get().strip())
            sale_price = response.xpath('//div[@class="game_area_purchase_game_wrapper"]//div['
                                        '@class="discount_final_price"]/text()')
            if len(sale_price) > 0:
                sale_price = re.sub(r'(\d+)(.*)', r'\1', sale_price[0].get().strip())
            else:
                sale_price = None
            platforms = response.xpath('//div[@class="game_area_purchase_game_wrapper"]//span[contains(@class, '
                                       '"platform_img")]/@class')
            pattern = re.compile(r"(platform_img )(\w+)")
            platforms = [s.get() for s in platforms]
            platforms = [re.sub(pattern, r'\2', s) for s in platforms]
            platforms = list(dict.fromkeys(platforms))
            item['tags'] = tags[::-1]
            item['price'] = price
            item['sale_price'] = sale_price
            item['available_platforms'] = platforms
            item['name'] = name[0].get()
            item['category'] = [s.get() for s in category[1:]]
            item['rating_of_game'] = rating
            item['number_of_reviews'] = number_of_reviews
            item['release_date'] = release_date
            item['developer'] = developer[0].get()
            yield item
