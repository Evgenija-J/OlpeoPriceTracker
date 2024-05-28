from product import Product


class User:

    def __init__(self, email, username, password):
        self.email = email,
        self.username = username,
        self.password = password,
        self.products = []

    def add_new_product(self, url):
        self.products.append(Product(url))

    def update_products_prices(self):
        for product in self.products:
            product.set_current_price()

