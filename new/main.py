name = 'Вася'

Name_fl_menu = 'menu.txt'

fl = open(Name_fl_menu, 'r', encoding='UTF-8')
Lines = fl.readlines()
fl.close()

# Формирование строки меню
str_menu = f'Дорогой {name} !!!\nКуда пойдём гулять?\n'
Lines.sort() # Сортировка списка в Алфавитном порядке
i = 1
for L in Lines:
	str1 = L.strip()
	str_menu +=f'\t {i}) ' + str1.upper()+'\n'
	i+=1
MAX_I = i+1

str_menu +=f'\t {i}) ' + 'Остаемся дома\nВведите номер выбранного меню'
# Вывод МЕНЮ ДЛЯ ПОЛЬЗОВАТЕЛЯ на экран
print(str_menu)
num = input()
# Обработка ответа пользователя
test = num.isdigit() # Проверка, является ли num числом
if (test): # Всё ХОРОШО, если num является числом
	num_int = int(num) - 1 # Преобразование num в целое число
	if ((num_int>=0) and (num_int<=MAX_I)): # Всё ХОРОШО, если число num_int АДЕКВАТНОЕ
		print(num_int)
		print(f'Дорогой {name}, мы ждём тебя в {Lines[num_int]}')
	elif (num==MAX_I): # Ответ при выборе "Остаёмся дома"
		print('Succesfully!')
	else: # Всё ПЛОХО, если число num_int НЕАДЕКВАТНОЕ
		print(f'Дорогой {name}, к сожалению такого варианта ответа не существует\nВведите корректное значение номера меню: ')
else: #Всё ПЛОХО, если num НЕ является числом
	print (f'Дорогой {name}, мы Вас не поняли\nВведите корректное значение номера меню: ')