from tkinter import *


class ProductsWindow:
    def __init__(self, root, db_handler):
        self.root = root

        self.root.title("Your products watchlist")
        self.root.resizable(False, False)
        self.root.config(bg="white", height=660, width=990)

        self.db_handler = db_handler

        self.canvas = Canvas(root, width=990, height=660, bg="white")
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.frame = Frame(self.canvas, bg="white", height=660, width=990)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", self.on_frame_configure)

        self.scrollbar_y = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.pack(side=RIGHT, fill=Y)
        self.canvas.config(yscrollcommand=self.scrollbar_y.set)

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.products = self.db_handler.get_user_products()

        self.y = 0
        self.display_products(self.y)

    def on_frame_configure(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def display_products(self, y):
        for product in self.products:
            text = product[2]
            color = 'gray45'
            name = Label(self.root, text=text,
                         font=('Open Sans', 8, 'bold'),
                         fg=color, bg='white')
            name.place(x=10, y=y)
            if product[4] != 0 or product[4] is not None:
                color = 'firebrick1'
            text = 'Initial price:   ' + str(product[3]) + '  |  ' + 'Discounted price:   ' + str(product[4])
            prices = Label(self.root, text=text,
                           font=('Open Sans', 8, 'bold'),
                           fg=color, bg='white')
            prices.place(x=10, y=y + 30)
            y += 90


if __name__ == '__main__':
    products_window = Tk()
    app = ProductsWindow(products_window)
    products_window.mainloop()
