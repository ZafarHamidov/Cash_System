import sqlite3

# Подключение к SQLite
conn = sqlite3.connect('cash_register.db')

# Создание объекта курсора
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""
CREATE TABLE IF NOT EXISTS Products(
    name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL);
""")

# Вставка некоторых продуктов
cursor.execute("INSERT INTO Products (name, price, quantity) VALUES (?, ?, ?)", ("яблоко", 0.5, 100))
cursor.execute("INSERT INTO Products (name, price, quantity) VALUES (?, ?, ?)", ("апельсин", 0.6, 80))
cursor.execute("INSERT INTO Products (name, price, quantity) VALUES (?, ?, ?)", ("банан", 0.3, 120))

# Применение изменений и закрытие подключения к файлу базы данных
conn.commit()
conn.close()
