import scrapy


class Game(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    rating_of_game = scrapy.Field()
    number_of_reviews = scrapy.Field()
    release_date = scrapy.Field()
    developer = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    sale_price = scrapy.Field()
    available_platforms = scrapy.Field()
