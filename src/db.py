import sqlite3
import os

productsList = [
    {"id": 1, "name": "Apple", "price": 4.15, "stock": 20},
    {"id": 2, "name": "Strawberry", "price": 6.50, "stock": 15},
    {"id": 3, "name": "Banana", "price": 1.95, "stock": 40},
    {"id": 4, "name": "Watermelon", "price": 9.80, "stock": 10},
    {"id": 5, "name": "Orange", "price": 3.75, "stock": 30},
    {"id": 6, "name": "Grape", "price": 2.25, "stock": 60},
]

dbPath = os.path.join(os.path.dirname(__file__), '..', 'data', 'salesSystemData.db')

def initDB():
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()

    cursor.execute('PRAGMA foreign_keys = ON;')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product (
        productId INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sale (
        saleId INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP),
        taxes REAL NOT NULL DEFAULT 0.0,
        discount REAL NOT NULL DEFAULT 0.0,
        total REAL NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productInSale (
        productId INTEGER NOT NULL,
        saleId INTEGER NOT NULL,
        count INTEGER NOT NULL,
        unitPrice INTEGER NOT NULL,
        FOREIGN KEY(saleId) REFERENCES sale(saleId),
        FOREIGN KEY(productId) REFERENCES product(productId)
            ON DELETE RESTRICT
            ON UPDATE CASCADE,
        PRIMARY KEY(productId, saleId)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        userId INTEGER NOT NULL PRIMARY KEY,
        userName TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL CHECK (role IN ('admin', 'seller', 'analyst'))
    )
    ''')

    cursor.execute('SELECT COUNT(*) FROM product;')
    count = cursor.fetchone()[0]

    if count == 0:
        for product in productsList:
            cursor.execute('INSERT INTO product (name, price, stock) VALUES (?, ?, ?);',
            (product["name"], product["price"], product["stock"]))
        
        cursor.execute('''INSERT INTO product (name, price, stock) VALUES ('Berries', 2.30, 45);''')
        conn.commit()

    conn.close()

def getAllProducts():
    with sqlite3.connect(dbPath) as conn:
        cursor = conn.cursor()
        result = cursor.execute('SELECT * FROM product')
        return result.fetchall()

def addProduct(product):
    with sqlite3.connect(dbPath) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO product (name, price, stock) VALUES (?, ?, ?);', (product[0], product[1], product[2]))

def delProduct(id):
    try:
        with sqlite3.connect(dbPath) as conn:
            cursor = conn.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            cursor.execute('DELETE FROM product WHERE productId = ?;', (id,))
    except sqlite3.IntegrityError:
        print("The element is used by other table, you can't delete it")

def getPrice(id):
    with sqlite3.connect(dbPath) as conn:
        cursor = conn.cursor()
        result = cursor.execute('SELECT name, price FROM product WHERE productId = ?', (id,))
        return result.fetchone()
        
def uptPrice(id, newPrice):
    with sqlite3.connect(dbPath) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE product SET price = ? WHERE productId = ?;', (newPrice, id))

def getStock(id):
    with sqlite3.connect(dbPath) as conn:
        cursor = conn.cursor()
        result = cursor.execute('SELECT name, stock FROM product WHERE productId = ?', (id,))
        return result.fetchone()

def uptStock(id, newStock):
    with sqlite3.connect(dbPath) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE product SET stock = ? WHERE productId = ?;', (newStock, id))

def useDataBase(query, params = None, returnLastId = False):
    with sqlite3.connect(dbPath) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        lastId = cursor.lastrowid

    if returnLastId:
        return lastId
    else:
        return results