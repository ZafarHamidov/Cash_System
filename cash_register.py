import sqlite3

# Переподключение к базе данных SQLite
conn = sqlite3.connect('cash_register.db')
cursor = conn.cursor()

# Новый словарь для отслеживания покупок
items = {}

grand_total = 0.0
while True:
    # Выводим все товары, их цены и количество
    cursor.execute("SELECT name, price, quantity FROM Products")
    products = cursor.fetchall()

    print("\nДоступные товары:")
    for product in products:
        print(f'Товар: {product[0]}, Цена: {round(product[1], 2)}, Количество доступно: {product[2]}')

    product_name = input('\nВведите название товара (или "exit" для завершения): ')
    
    if product_name.lower() == 'exit':
        break

    quantity = int(input('Введите количество: '))
    
    # Ищем товар в базе данных
    cursor.execute("SELECT price, quantity FROM Products WHERE name=?", (product_name,))
    result = cursor.fetchone()
    
    if result is None:
        print("Такого товара нет в базе данных.")
        continue

    if quantity > result[1]:
        print("Извините, недостаточное количество данного товара в наличии.")
        continue

    price = result[0]
    total = round(price * quantity, 2)
    grand_total += total

    # Вычитаем купленное количество из доступного количества в базе данных
    new_quantity = result[1] - quantity
    cursor.execute("UPDATE Products SET quantity=? WHERE name=?", (new_quantity, product_name))
    conn.commit()

    # Добавляем или обновляем количество и общую стоимость этого товара в словаре items
    if product_name in items:
        items[product_name]['quantity'] += quantity
        items[product_name]['total'] = round(items[product_name]['total'] + total, 2)
    else:
        items[product_name] = {'price': round(price, 2), 'quantity': quantity, 'total': total}

# Закрываем подключение к файлу базы данных
conn.close()

# Выводим все товары, количество, цены и итоги
print('\nЧек:')
print('=====================================')
for name, info in items.items():
    print(f'Товар: {name}, Количество: {info["quantity"]}, Цена за единицу: {round(info["price"], 2)}, Итого: {round(info["total"], 2)}')
print('=====================================')
print('Общая сумма: ', round(grand_total, 2))
