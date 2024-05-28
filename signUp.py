import tkinter.messagebox
from tkinter import *
from PIL import ImageTk
from databaseHandler import DatabaseHandler


class SignUpWindow:
    def __init__(self, root):
        self.root = root
        self.root.title('Sign up page')
        self.root.resizable(False, False)

        self.db_handler = DatabaseHandler()

        self.background = ImageTk.PhotoImage(file='Images/bg.jpg')
        self.bg_label = Label(root, image=self.background)
        self.bg_label.grid()

        self.frame = Frame(root, bg='white')
        self.frame.place(x=554, y=100)

        self.create_widgets()

    def create_widgets(self):
        self.heading = Label(self.frame, text='CREATE AN ACCOUNT',
                             font=('Microsoft Yahei UI Light', 18, 'bold'), bg='white', fg='gray45')
        self.heading.grid(row=0, column=0, padx=13, pady=10)

        self.create_entry('Email', 1)
        self.email_entry = self.create_entry_box(2)

        self.create_entry('Username', 3, pady=(10, 0))
        self.username_entry = self.create_entry_box(4)

        self.create_entry('Password', 5, pady=(10, 0))
        self.password_entry = self.create_entry_box(6, show='*')

        self.create_entry('Confirm Password', 7, pady=(10, 0))
        self.confirm_password_entry = self.create_entry_box(8, show='*')

        self.create_signup_button()
        self.create_login_link()

    def create_entry(self, text, row, pady=0):
        label = Label(self.frame, text=text,
                      font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white', fg='gray45')
        label.grid(row=row, column=0, sticky='w', padx=25, pady=pady)

    def create_entry_box(self, row, show=None):
        entry = Entry(self.frame, width=30, font=('Microsoft Yahei UI Light', 10, 'bold'),
                      fg='white', bg='gray45', show=show)
        entry.grid(row=row, column=0, sticky='w', padx=25)
        return entry

    def create_signup_button(self):
        signup_button = Button(self.frame, text='Signup', font=('Microsoft Yahei UI Light', 16, 'bold'),
                               bd=0, bg='gray45', fg='white', width=18,
                               activebackground='white', activeforeground='white',
                               command=self.connect_database)
        signup_button.grid(row=10, column=0, pady=50)

    def create_login_link(self):
        already_have_account = Label(self.frame, text="Already have an account?", font=('Open Sans', 9, 'bold'),
                                     bg='white', fg='gray45')
        already_have_account.grid(row=11, column=0, sticky='w', padx=25, pady=10)

        login_button = Button(self.frame, text='Log in',
                              font=('Open Sans', 8, 'bold underline'),
                              fg='blue', bg='white',
                              activeforeground='blue',
                              activebackground='white',
                              cursor='hand2', bd=0, command=self.login_page)
        login_button.grid(row=11, column=0, sticky='e', padx=50)

    def clear(self):
        self.email_entry.delete(0, END)
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.confirm_password_entry.delete(0, END)

    def connect_database(self):
        if not self.all_fields_filled():
            tkinter.messagebox.showerror('Error', 'All fields are required!')
        elif self.password_entry.get() != self.confirm_password_entry.get():
            tkinter.messagebox.showerror('Error', 'Password mismatch')
        else:
            if self.db_handler.connect():
                if self.db_handler.setup_database():
                    if self.db_handler.signup_user(self.email_entry.get(), self.username_entry.get(),
                                                   self.password_entry.get()):
                        tkinter.messagebox.showinfo('Success', 'Registration is successful')
                        self.clear()
                        self.login_page()
                self.db_handler.close()

    def all_fields_filled(self):
        return all([
            self.email_entry.get(),
            self.username_entry.get(),
            self.password_entry.get(),
            self.confirm_password_entry.get()
        ])

    def login_page(self):
        self.root.destroy()
        login_window = Tk()
        self.load_login_page(login_window)
        login_window.mainloop()

    def load_login_page(self, login_window):
        from logIn import LoginWindow
        app = LoginWindow(login_window)


if __name__ == '__main__':
    signup_window = Tk()
    app = SignUpWindow(signup_window)
    signup_window.mainloop()

