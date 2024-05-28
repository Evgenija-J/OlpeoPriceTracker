import requests
from bs4 import BeautifulSoup


class Scraper:

    def __init__(self, url):
        self.header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
        }
        self.response = requests.get(url, headers=self.header)
        self.soup = BeautifulSoup(self.response.content, 'lxml')

    def extract_price(self, price):
        price = price.replace('.', '').replace('ден', '')
        return int(price)

    def scrape_prices(self):
        regular_price_element = self.soup.find('del').find('span', class_="woocommerce-Price-amount amount").contents
        discounted_price_element = self.soup.find('ins').find('span', class_="woocommerce-Price-amount amount").contents

        regular_price = None
        discounted_price = None

        if regular_price_element:
            regular_price = self.extract_price(regular_price_element[0])

        if discounted_price_element:
            discounted_price = self.extract_price(discounted_price_element[0])

        return regular_price, discounted_price

    def scrape_name(self):
        return self.soup.find(class_="product_title entry-title").get_text()

    def scrape_stock(self):
        return self.soup.find(class_="stock").get_text()
