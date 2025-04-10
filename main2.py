import random
import os
import hashlib

products = os.path.join('products.txt')
DATABASE_FILE = os.path.join('source', 'databases', 'database01.txt')

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

def print_products(products):
    try:
        with open(products, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        formatted_output = []
        for line in lines:
            parts = line.strip().split(' ')
            if len(parts) == 2: 
                item_name, item_price = parts
                formatted_output.append(f"{item_name}: {item_price}$")
        
        result = " | ".join(formatted_output) + " |"
        print(result)  # Выводим результат

    except FileNotFoundError:
        print("Файл не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def print_receipt(cart):
    total = sum(cart.values())
    print("\n----Чек----")
    for item, price in cart.items():
        print(f"• {item}: {price:.2f}₽")
    print(f"Итого: {total:.2f}₽")
    return total

def save_receipt(cart, total):
    receipt_id = random.randint(100000, 999999)
    file_name = f"Чек_{receipt_id}.txt"
    with open(file_name, 'w', encoding='UTF-8') as file:
        file.write("----Чек----\n")
        for item, price in cart.items():
            file.write(f"{item}: {price:.2f}₽\n")
        file.write(f"Итого: {total:.2f}₽\n")
    print(f"Чек сохранён в файл: {file_name}")

def load_products(file_name):
    products = {}
    try:
        with open(file_name, 'r', encoding='UTF-8') as file:
            for line in file:
                parts = line.strip().split(' ')
                if len(parts) == 2:
                    name, price = parts
                    products[name.lower()] = float(price)  
    except FileNotFoundError:
        print("Файл товаров не найден.")
    except Exception as e:
        print(f"Произошла ошибка при загрузке товаров: {e}")
    return products

# ...

def main():
    cart = {}
    clear_console()
    users = load_users()
    products = load_products("products.txt")  
    
    while True:
        action = input("Добро пожаловать!\n{1}--Войти\n{2}--Зарегистрироваться\n\n>> ")
        if action == '1':
            login_user(users)
            break
        elif action == '2':
            register_user(users)
            users = load_users()
            break
        else:
            print("Пожалуйста, выберите 1 или 2.")

    while True:
        print("\nДоступные товары:")
        print_products("products.txt")
        
        if not cart:
            print('\nВаша корзина пустая :(')
            print('Желаете что-нибудь приобрести?')
        else:
            print("\n----Корзина----")
            for name, price in cart.items():
                print(f"{name}: {price:.2f}₽")

        print("\nДействия с корзиной:")
        print("[1] Добавить товар в корзину")
        print("[2] Убрать товар из корзины")
        print("[3] Посмотреть корзину")
        print("[4] Распечатать чек")
        choice = input(">> ")
        
        if choice == '1':
            product_name = input('\nНазвание товара: ').lower()
            if product_name in products:
                quantity = int(input('Количество: '))
                cart[product_name.capitalize()] = products[product_name] * quantity  
                print(f'{product_name.capitalize()} добавлен(о) в корзину.')
            else:
                print('\nДанный товар не существует')

        elif choice == '2':
            product_name_input = input('\nНазвание товара: ').lower()
            product_name_in_cart = None
            for name in cart.keys():
                if name.lower() == product_name_input:
                    product_name_in_cart = name
                    break
            
            if product_name_in_cart:
                del cart[product_name_in_cart]
                print(f'{product_name_in_cart} удален(о) из корзины')
            else:
                print('Этот товар не в корзине.')

        elif choice == '3':
            if not cart:
                print('\nВаша корзина пустая :(')
                print('Желаете что-нибудь приобрести?')
            else:
                print("\n----Корзина----")
                for name, price in cart.items():
                    print(f"{name}: {price:.2f}₽")

        elif choice == '4':
            total_price = print_receipt(cart)
            confirm = input('\nВы подтверждаете покупку? (Y/n)\n>> ')
            if confirm.lower() == 'y':
                clear_console()
                print('Спасибо за покупку!\nВаш чек')
                print_receipt(cart)
                save_receipt(cart, total_price)
                break
            elif confirm.lower() == 'n':
                print()
            else:
                print('[!] Такого варианта ответа не существует')

        else:
            print("\nПожалуйста, выберите допустимую опцию.")
        
        input('\n[!] Нажмите ENTER для продолжения')
        clear_console()

if __name__ == "__main__":
    main()