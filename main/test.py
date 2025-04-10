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