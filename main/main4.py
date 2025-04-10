import random
import os
import hashlib
from datetime import datetime
import pytz
 
# Часовые пояса
moscow_tz = pytz.timezone('Europe/Moscow')

# Путь к файлам
products_name = os.path.join('products2.txt')
DATABASE_FILE = os.path.join('source', 'databases', 'database01.txt')

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_date(timezone):
    current_date = datetime.now(timezone)
    formatted_date = current_date.strftime('%Y-%m-%d_%H-%M-%S')
    return formatted_date

def hash_password(password, salt):
    return hashlib.sha256((salt + password).encode()).hexdigest()

def load_users():
    users = {}
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r', encoding='UTF-8') as file:
            for line in file:
                parts = line.strip().split(':')
                if len(parts) == 4:
                    login, salt, hashed_password, hashed_second_password = parts
                    users[login] = (salt, hashed_password, hashed_second_password)
                else:
                    print(f"Некорректная запись в файле: {line.strip()}")
    return users

def login_user(users):
    while True:
        clear_console()
        print('\n-----Авторизация-----')
        login = input("Логин: ")
        if login in users:
            password = input("Пароль: ")
            second_password = input("Второй пароль: ")
            salt, hashed_password, hashed_second_password = users[login]
            hashed_input_password = hash_password(password, salt)
            hashed_input_second_password = hash_password(second_password, salt)
            if hashed_input_password == hashed_password and hashed_input_second_password == hashed_second_password:
                print("Авторизация успешна!")
                input('\n[!] Нажмите ENTER для продолжения')
                clear_console()
                return True
            else:
                input("Один из паролей неверный. Попробуйте снова.\n[!] Нажмите ENTER для продолжения")
                clear_console()
        else:
            print("Пользователь не найден.")
            action = input("Хотите зарегистрироваться? (Y/n)\n>> ")
            if action.lower() == 'y':
                register_user(users)
                users = load_users()
                break
            else:
                print("Возврат в главное меню.")
                clear_console()
                continue

def register_user(users):
    while True:
        print('\n-----Регистрация-----')
        login = input("Логин: ")
        if login in users:
            print("Этот логин уже занят. Попробуйте другой.")
            continue
        password = input("Пароль: ")
        second_password = input("Второй пароль: ")
        salt = os.urandom(16).hex()
        hashed_password = hash_password(password, salt)
        hashed_second_password = hash_password(second_password, salt)
        with open(DATABASE_FILE, 'a', encoding='UTF-8') as file:
            file.write(f"{login}:{salt}:{hashed_password}:{hashed_second_password}\n")
        print("Регистрация успешна!")
        input('\n[!] Нажмите ENTER для продолжения')
        clear_console()
        return login

def print_products(products_file):
    try:
        if not os.path.exists(products_file):
            print("Файл с товарами не найден. Пожалуйста, проверьте его наличие.")
            return
        
        with open(products_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        if not lines:
            print("Список товаров пуст.")
            return
        
        formatted_output = []
        for index, line in enumerate(lines, start=1):
            parts = line.strip().split(':')
            if len(parts) == 2:
                item_name, item_price = parts
                item_name = item_name.strip().strip('"')
                try:
                    item_price = float(item_price.strip())
                except ValueError:
                    print(f"Ошибка: некорректная цена для товара '{item_name}'. Пропускаем...")
                    continue
                formatted_output.append(f"{index}) {item_name}: {item_price}₽")
        
        result = " | ".join(formatted_output) + " |"
        print(result)
    
    except Exception as e:
        print(f"Произошла ошибка при выводе товаров: {e}")

def print_receipt(cart):
    if not cart:
        print("Корзина пуста. Невозможно распечатать чек.")
        input('\n[!] Нажмите ENTER для продолжения')
        clear_console()
        return None
    total = sum(details['price'] * details['quantity'] for details in cart.values())
    receipt_date = get_date(moscow_tz)
    print(f"\nЧек ({receipt_date}):")
    for item, details in cart.items():
        print(f"• {item}: {details['price']:.2f}₽ x {details['quantity']}шт. = {details['price'] * details['quantity']:.2f}₽")
    print(f"Итого: {total:.2f}₽")
    return total

def save_receipt(cart, total):
    if not cart:
        print("Корзина пуста. Чек не может быть сохранён.")
        input('\n[!] Нажмите ENTER для продолжения')
        clear_console()
        return
    receipt_id = random.randint(100000, 999999)
    receipt_date = get_date(moscow_tz)
    file_name = f"Чек_{receipt_date}_({receipt_id}).txt"
    with open(file_name, 'w', encoding='UTF-8') as file:
        file.write(f"ФЕДОР ШОП\nКАССОВЫЙ ЧЕК ПРИХОД:\n")
        file.write(f'Наименование | Кол-во | Цена | Стоимость\n')
        for item, details in cart.items():
            price_per_unit = details['price']
            quantity = details['quantity']
            total_price_for_item = price_per_unit * quantity
            file.write(f"{item}   {quantity:.3f}шт   {price_per_unit:.2f}   {total_price_for_item:.2f}\n")
        file.write(f"ИТОГ:----------------------{total:.2f}\nСУММА НДС 20%\n{receipt_date}\n")
        file.write(f'\nООО "ФЕДОР КОРПАРЕЙШН" 644042, г.Омск, Набережная.Иртышская, д. 10, к.1')
        file.write(f"\n(дополнительная юридическая информация)")
    print(f"\nЧек сохранён в файл: {file_name}")

def load_products(file_name):
    products = {}
    try:
        if not os.path.exists(file_name):
            print("Файл товаров не найден.")
            return products
        with open(file_name, 'r', encoding='UTF-8') as file:
            for index, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(':')
                if len(parts) == 2:
                    name, price = parts
                    name = name.strip().strip('"')
                    try:
                        price = float(price.strip())
                    except ValueError:
                        print(f"Ошибка: некорректная цена для товара '{name}' в строке {index}. Пропускаем...")
                        continue
                    products[index] = {'name': name, 'price': price}
                else:
                    print(f"Ошибка: некорректный формат строки '{line}' в строке {index}. Пропускаем...")
    
    except Exception as e:
        print(f"Произошла ошибка при загрузке товаров: {e}")
    
    return products

def add_to_cart(cart, products):
    try:
        selected_index = int(input("\nВведите индекс товара для добавления в корзину: "))
        if selected_index in products:
            quantity = int(input("Введите количество: "))
            product = products[selected_index]
            if product['name'] in cart:
                cart[product['name']]['quantity'] += quantity
            else:
                cart[product['name']] = {'price': product['price'], 'quantity': quantity}
            print(f"{quantity} шт. {product['name']} добавлено в корзину.")
        else:
            print("Неверный индекс товара!")
    except ValueError:
        print("Пожалуйста, введите корректный индекс или количество.")

def remove_from_cart(cart):
    if not cart:
        print("Корзина пуста. Нечего удалять.")
        return
    print("\nТовары в корзине:")
    for index, (name, details) in enumerate(cart.items(), start=1):
        print(f"{index}) {name}: {details['price']:.2f}₽ x {details['quantity']}шт.")
    try:
        selected_index = int(input("\nВведите номер товара для удаления: "))
        if 1 <= selected_index <= len(cart):
            item_to_remove = list(cart.keys())[selected_index - 1]
            removed_item = cart.pop(item_to_remove)
            print(f"Товар '{item_to_remove}' удален из корзины. Сумма: {removed_item['price'] * removed_item['quantity']:.2f}₽")
        else:
            print("Неверный номер товара!")
    except ValueError:
        print("Пожалуйста, введите корректный номер.")
        
def main():
    cart = {}
    clear_console()
    if not os.path.exists(products_name):
        print("Файл с товарами не найден. Программа завершает работу.")
        return
    users = load_users()
    products = load_products(products_name)
    if not products:
        print("Список товаров пуст. Программа завершает работу.")
        return
    while True:
        action = input("Добро пожаловать!\n{1}--Войти\n{2}--Зарегистрироваться\n>> ")
        if action == '1':
            if login_user(users):
                break
        elif action == '2':
            register_user(users)
            users = load_users()
            break
        else:
            print("Пожалуйста, выберите 1 или 2.")
    while True:
        print("\nДоступные товары:")
        print_products(products_name)
        if not cart:
            print('\nВаша корзина пустая :(')
            print('Желаете что-нибудь приобрести?')
        else:
            print("\n----Корзина----")
            for index, (name, details) in enumerate(cart.items(), start=1):
                print(f"{index}) {name}: {details['price']:.2f}₽ x {details['quantity']}шт.")
        print("\nДействия с корзиной:")
        print("[1] Добавить товар в корзину")
        print("[2] Убрать товар из корзины")
        print("[3] Посмотреть корзину")
        print("[4] Распечатать чек")
        print("[5] Выход")
        choice = input(">> ")
        if choice == '1':
            add_to_cart(cart, products)
        elif choice == '2':
            remove_from_cart(cart)
        elif choice == '3':
            if not cart:
                print('\nВаша корзина пустая :(')
                print('Желаете что-нибудь приобрести?')
            else:
                print("\n----Корзина----")
                for index, (name, details) in enumerate(cart.items(), start=1):
                    print(f"{index}) {name}: {details['price']:.2f}₽ x {details['quantity']}шт.")
        elif choice == '4':
            total_price = print_receipt(cart)
            if total_price is not None:
                confirm = input("Хотите сохранить чек? (Y/n): ").strip().lower()
                if confirm == 'y':
                    save_receipt(cart, total_price)
                    cart.clear()
                    print('(Корзина была очищена.)')
                elif confirm == 'n':
                    print("Покупка отменена.")
                else:
                    print('[!] Такого варианта ответа не существует')
        elif choice == '5':
            print("Выход из программы.")
            break
        else:
            print("\nПожалуйста, выберите допустимую опцию.")
        input('\n[!] Нажмите ENTER для продолжения')
        clear_console()

if __name__ == "__main__":
    main()