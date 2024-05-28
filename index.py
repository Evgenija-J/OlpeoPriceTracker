import databaseHandler
from tkinter import *

from product import Product
from productsFrame import ProductsWindow


class MainWindow:
    def __init__(self, root, db_handler=databaseHandler.DatabaseHandler()):
        self.root = root

        self.root.title("Welcome to Eva's skin care price tracker")
        self.root.resizable(False, False)
        self.root.config(bg="white", height=660, width=990)

        self.db_handler = db_handler

        self.create_widgets()



    def create_widgets(self):
        self.product_url_entry = self.create_entry_box()
        self.heading = Label(self.root, text='WELCOME!',
                             font=('Microsoft Yahei UI Light', 30, 'bold'), bg='white', fg='gray45')
        self.heading.place(x=370, y=70)

        self.create_add_product_to_watchlist_button()
        self.create_view_watchlist_button()

        self.create_entry()

    def create_entry(self):
        label = Label(self.root, text='Product URL',
                      font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white', fg='gray45')
        label.place(x=100, y=190)

    def create_entry_box(self):
        entry = Entry(self.root, width=75, font=('Microsoft Yahei UI Light', 13, 'bold'),
                      fg='white', bg='gray70')
        entry.place(x=100, y=220)
        return entry

    def create_add_product_to_watchlist_button(self):
        add_product_button = Button(self.root, text='Add product to watchlist',
                                    font=('Microsoft Yahei UI Light', 13, 'bold'),
                                    bd=2, bg='gray45', fg='white', width=19,
                                    activebackground='white', activeforeground='white',
                                    relief='groove', command=self.check_add_product_button)
        add_product_button.place(x=635, y=260)

    def check_add_product_button(self):
        url = self.product_url_entry.get()
        if url:
            return self.db_handler.insert_product(Product(url))
        return False

    def create_view_watchlist_button(self):
        watchlist_button = Button(self.root, text='View watchlist',
                                    font=('Microsoft Yahei UI Light', 13, 'bold'),
                                    bd=2, bg='firebrick1', fg='white', width=18,
                                    activebackground='white', activeforeground='white',
                                    relief='groove', command=self.open_products_window)
        watchlist_button.place(x=370, y=450)

    def open_products_window(self):
        products_window = ProductsWindow(self.root, self.db_handler)


if __name__ == '__main__':
    main_window = Tk()
    app = MainWindow(main_window)
    main_window.mainloop()
