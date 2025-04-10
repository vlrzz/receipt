import random
import os
import hashlib

# Путь к файлам
DATABASE_FILE = os.path.join('source', 'databases', 'database01.txt')
PRODUCTS_FILE = 'prd.txt'

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

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

def register_user(users):
    while True:
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

def login_user(users):
    while True:
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
                print("Неверный пароль или второй пароль. Попробуйте снова.")
        else:
            print("Пользователь не найден.")
            action = input("Хотите зарегистрироваться? (Да/Нет)\n>> ")
            if action.lower() == 'да':
                register_user(users)
                users = load_users()
            else:
                print("Возврат в главное меню.")
                continue

def load_products():
    products = {}
    with open(PRODUCTS_FILE, 'r', encoding='UTF-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(':')
                if len(parts) == 3:
                    product_id, name, price = parts
                    products[name.upper()] = float(price)
                else:
                    print(f"Некорректная строка в файле продуктов: {line}")
    return products

def print_products(products):
    print("\nДоступные товары:")
    max_name_length = max(len(name) for name in products.keys())
    for index, (name, price) in enumerate(products.items(), start=1):
        dashes = '-' * (40 - len(name))
        print(f"{index}. {name:<{max_name_length}} {dashes} {price:>6.2f}₽")

def print_receipt(cart):
    total = sum(cart.values())
    print("\n----Чек----")
    for index, (item, price) in enumerate(cart.items(), start=1):
        print(f"{index}. • {item}: {price:.2f}₽")
    print(f"Итого: {total:.2f}₽")
    return total

def save_receipt(cart, total):
    receipt_id = random.randint(100000, 999999)
    file_name = f"Чек_{receipt_id}.txt"
    with open(file_name, 'w', encoding='UTF-8') as file:
        file.write("----Чек----\n")
        for index, (item, price) in enumerate(cart.items(), start=1):
            file.write(f"{index}. {item}: {price:.2f}₽\n")
        file.write(f"Итого: {total:.2f}₽\n")
    print(f"Чек сохранён в файл: {file_name}")

def main():
    cart = {}
    clear_console()

    users = load_users()

    # Меню входа и регистрации
    while True:
        action = input("Добро пожаловать!\n{1}--Войти\n{2}--Зарегистрироваться\n\n>> ")
        if action == '1':
            login_user(users)
            break
        elif action == '2':
            register_user(users)
            users = load_users()
        else:
            print("Пожалуйста, выберите 1 или 2.")

    products = load_products()

    while True:
        print_products(products)

        if not cart:
            print('\nВаша корзина пустая :(')
            print('Желаете что-нибудь приобрести?')
        else:
            print("\n----Корзина----")
            for index, (name, price) in enumerate(cart.items(), start=1):
                print(f"{index}. {name}: n{price:.2f}₽")

        print("\nДействия с корзиной:")
        print("[1] Добавить товар в корзину")
        print("[2] Убрать товар из корзины")
        print("[3] Посмотреть корзину")
        print("[4] Распечатать чек")
        choice = input(">> ")

        if choice == '1':
            product_index = int(input('\nВыберите номер товара: ')) - 1
            if 0 <= product_index < len(products):
                product_name = list(products.keys())[product_index]
                quantity = int(input('Количество: '))
                cart[product_name] = cart.get(product_name, 0) + products[product_name] * quantity
                print(f'{product_name} добавлен(о) в корзину.')
            else:
                print('\nДанный товар не существует')
        elif choice == '2':
            item_index = int(input('\nВведите номер товара для удаления: ')) - 1
            if 0 <= item_index < len(cart):
                product_name = list(cart.keys())[item_index]
                del cart[product_name]
                print(f'{product_name} удален(о) из корзины')
            else:
                print('Некорректный номер товара.')
        elif choice == '3':
            if not cart:
                print('\nВаша корзина пустая :(')
                print('Желаете что-нибудь приобрести?')
            else:
                print("\n----Корзина----")
                for index, (name, price) in enumerate(cart.items(), start=1):
                    print(f"{index}. {name}: {price:.2f}₽")
        elif choice == '4':
            total_price = print_receipt(cart)
            confirm = input('\nВы подтверждаете покупку? (Да/Нет)\n>> ')
            if confirm.lower() == 'да':
                clear_console()
                print('Спасибо за покупку!\nВаш чек:')
                print_receipt(cart)
                save_receipt(cart, total_price)
                break
            elif confirm.lower() == 'нет':
                print()
            else:
                print('[!] Такого варианта ответа не существует')
        else:
            print("\nПожалуйста, выберите допустимую опцию.")
        
        input('\n[!] Нажмите ENTER для продолжения')
        clear_console()

if __name__ == "__main__":
    main()
