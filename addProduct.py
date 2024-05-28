from tkinter import *

from PIL import ImageTk

from databaseHandler import DatabaseHandler


class AddProductWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Add a new product")
        self.root.resizable(False, False)

        self.db_handler = DatabaseHandler()

        self.background = ImageTk.PhotoImage(file='Images/background.jpg')
        self.bg_label = Label(root, image=self.background)
        self.bg_label.grid()

        self.create_widgets()

    def create_widgets(self):

        self.create_label()
        self.create_entry_box()



    def create_label(self):
        label = Label(self.root, text='Product URL',
                      font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white', fg='gray45')
        label.place(x=100, y=100)

    def create_entry_box(self):
        entry = Entry(self.root, width=30, font=('Microsoft Yahei UI Light', 10, 'bold'),
                      fg='white', bg='gray45')
        entry.place(x=100, y=120)
        return entry


if __name__ == '__main__':
    add_product_window = Tk()
    app = AddProductWindow(add_product_window)
    add_product_window.mainloop()