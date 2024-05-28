import pymysql
from tkinter import messagebox
from user import User


class DatabaseHandler:
    def __init__(self, host='localhost', user='root', password='MySqlG2021*7', database='skincare_app_data'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.current_app_user_id = None

    def connect(self):
        try:
            self.connection = pymysql.connect(host=self.host,
                                              user=self.user,
                                              password=self.password,
                                              database=self.database)
            self.cursor = self.connection.cursor()
        except pymysql.MySQLError as e:
            self.connection = pymysql.connect(host=self.host,
                                              user=self.user,
                                              password=self.password)
            self.cursor = self.connection.cursor()
            self.setup_database()
            return False
        return True

    def setup_database(self):
        try:
            self.cursor.execute('CREATE DATABASE IF NOT EXISTS skincare_app_data')
            self.cursor.execute('USE skincare_app_data')
            self.cursor.execute(
                'CREATE TABLE IF NOT EXISTS users ('
                'id INT AUTO_INCREMENT PRIMARY KEY, '
                'email VARCHAR(50), '
                'username VARCHAR(100), '
                'password VARCHAR(20), '
                'urls VARCHAR(10000))'
                )
            self.cursor.execute(
                'CREATE TABLE IF NOT EXISTS user_products ('
                'id INT AUTO_INCREMENT PRIMARY KEY, '
                'user_id INT NOT NULL, '
                'name VARCHAR(100), '
                'initial_price INT,'
                'current_price INT, '
                'stock VARCHAR(20), '
                'FOREIGN KEY (user_id) REFERENCES users(id))'
            )
            self.connect()
        except pymysql.MySQLError as e:
            messagebox.showerror('Error', f'Error creating database or table: {e}')
            return False
        return True

    def insert_user(self, user):
        if self.cursor is None:
            self.connection = pymysql.connect(host=self.host,
                                              user=self.user,
                                              password=self.password)
            self.cursor = self.connection.cursor()
        try:
            self.cursor.execute(
                'INSERT INTO users (email, username, password) VALUES (%s, %s, %s)',
                (user.email, user.username, user.password)
            )
        except pymysql.MySQLError as e:
            messagebox.showerror('Error', f'Error inserting user into database: {e}')
            return False

    def signup_user(self, email, username, password):
        try:
            self.cursor.execute('SELECT * FROM users WHERE username=%s', (username, ))
            if self.cursor.fetchone():
                messagebox.showerror('Error', 'Username already exists')
                return False
            self.insert_user(User(email, username, password))
            self.connection.commit()
        except pymysql.MySQLError as e:
            messagebox.showerror('Error', f'Error inserting data: {e}')
            return False
        return True

    def login_user(self, username, password):
        if not self.connect():
            return False
        query = 'SELECT * FROM users WHERE username=%s AND password=%s'
        self.cursor.execute(query, (username, password))
        row = self.cursor.fetchone()
        self.close()
        self.current_app_user_id = row[0]
        if row is None:
            messagebox.showerror('Error', 'Invalid username or password')
            return False
        messagebox.showinfo('Welcome', 'Successful login')
        return True

    def insert_product(self, product):
        if not self.connect():
            return False

        query = 'SELECT * FROM user_products WHERE user_id = %s AND name = %s'
        self.cursor.execute(query, (self.current_app_user_id, product.name))
        existing_product = self.cursor.fetchone()

        if existing_product:
            # If product with the same name exists for the same user, show an error message
            messagebox.showerror('Error', 'Product with the same name already exists for this user.')
            return False

        try:
            query =\
                'INSERT INTO user_products (user_id, name, initial_price, current_price, stock) VALUES (%s, %s, %s, %s, %s)'
            self.cursor.execute(query,
                (self.current_app_user_id, product.name, product.initial_price, product.current_price, product.stock)
            )
            self.connection.commit()
            self.close()
            return True
        except pymysql.MySQLError as e:
            messagebox.showerror('Error', f'Error inserting product into database: {e}')
            return False

    def get_user_products(self):
        if not self.connect():
            return False

        try:
            query = 'SELECT * FROM user_products WHERE user_id = %s'
            self.cursor.execute(query, (self.current_app_user_id,))
            products = self.cursor.fetchall()
            return products
        except pymysql.MySQLError as e:
            messagebox.showerror('Error', f'Error retrieving user products: {e}')
            return []

    def close(self):
        if self.connection:
            self.connection.close()
