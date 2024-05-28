import tkinter.messagebox
from tkinter import *
from PIL import ImageTk
from databaseHandler import DatabaseHandler
from signUp import SignUpWindow


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry('990x660+50+50')
        self.root.resizable(width=0, height=0)
        self.root.title('Login page')

        self.db_handler = DatabaseHandler()

        self.bg_image = ImageTk.PhotoImage(file='Images/bg.jpg')
        self.bg_label = Label(root, image=self.bg_image)
        self.bg_label.place(x=0, y=0)

        self.create_widgets()

    def create_widgets(self):
        heading = Label(self.root, text='USER LOGIN',
                        font=('Microsoft Yahei UI Light', 23, 'bold'),
                        bg='white', fg='gray45')
        heading.place(x=605, y=120)

        self.username_entry = self.create_entry('Username', 200)
        self.password_entry = self.create_entry('Password', 260, show='*')

        eye = PhotoImage(file='Images/closeye.png')
        eye_button = Button(self.root, image=eye,
                            bd=0, bg='white',
                            activebackground='white', cursor='hand2',
                            command=self.toggle_password_visibility)
        eye_button.place(x=800, y=255)

        login_button = Button(self.root, text='Login',
                              font=('Open Sans', 16, 'bold'),
                              fg='white', bg='gray45',
                              activeforeground='white', activebackground='white',
                              cursor='hand2', bd=0, width=19, command=self.login_user)
        login_button.place(x=578, y=350)

        sign_up_label = Label(self.root, text="Don't have an account?",
                              font=('Open Sans', 8, 'bold'),
                              fg='gray45', bg='white')
        sign_up_label.place(x=578, y=500)

        create_account_button = Button(self.root, text='Create account',
                                       font=('Open Sans', 8, 'bold underline'),
                                       fg='blue', bg='white',
                                       activeforeground='blue', activebackground='white',
                                       cursor='hand2', bd=0, command=self.signup_page)
        create_account_button.place(x=727, y=499)

    def create_entry(self, text, y, show=None):
        entry = Entry(self.root, width=25,
                      font=('Microsoft Yahei UI Light', 11, 'bold'),
                      bg='white', fg='gray45', bd=0, show=show)
        entry.place(x=580, y=y)
        entry.insert(0, text)
        underline = Frame(self.root, width=250, height=2)
        underline.place(x=580, y=y+22)
        entry.bind('<FocusIn>', lambda event, e=entry, t=text: self.on_entry_focus_in(e, t))
        entry.bind('<FocusOut>', lambda event, e=entry, t=text: self.on_entry_focus_out(e, t))
        return entry

    def on_entry_focus_in(self, entry, text):
        if entry.get() == text:
            entry.delete(0, END)

    def on_entry_focus_out(self, entry, text):
        if entry.get() == '':
            entry.insert(0, text)

    def toggle_password_visibility(self):
        if self.password_entry.cget('show') == '':
            self.password_entry.config(show='*')
        else:
            self.password_entry.config(show='')

    def signup_page(self):
        self.root.destroy()
        signup_window = Tk()
        app = SignUpWindow(signup_window)
        signup_window.mainloop()

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == '' or password == '':
            tkinter.messagebox.showerror('Error', 'All fields are required')
            return
        if self.db_handler.login_user(username, password):
            self.main_page()

    def main_page(self):
        self.root.destroy()
        main_window = Tk()
        self.load_main_page(main_window)
        main_window.mainloop()

    def load_main_page(self, main_window):
        from index import MainWindow
        app = MainWindow(main_window, self.db_handler)


if __name__ == '__main__':
    login_window = Tk()
    app = LoginWindow(login_window)
    login_window.mainloop()
