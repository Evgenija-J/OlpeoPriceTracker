from scraper import Scraper


class Product:

    def __init__(self, url):
        self.scraper = Scraper(url)
        self.name = self.scraper.scrape_name()
        self.initial_price, self.current_price = self.scraper.scrape_prices()
        self.stock = self.scraper.scrape_stock()

