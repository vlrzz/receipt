from datetime import date
from datetime import datetime
now = datetime.now()
today = date.today()
#-----Определение констант
Nsmv = 55
imax = 5
str_pt = 'сохранить чек?\n\t 0-сохранить\n\t любой символ-продолжить выбор\n\t 2-убрать товар'
str_cont='вы хотите завершить работу?\n\t 0-завершить работу\n\t любой символ-продолжить работу'
str_cont_2='желаете продолжить выбор?\n\t 0-завершить выбор \n\t любой символ-продолжить выбор'
str_cont_1='куда пойдём гулять?\n\t 1)в кино\n\t 2)на напережную\n\t 3)на пляж \n\t 4)в парк \n\t 5)в торговый центр\n\t 6)идём гулять в рощу \n\t 7)идём гулять в скейт парк \n\t 8)в бар \n\t 9)идем гулять на работе \n\t 10)никуда не идём, сидим дома'
str_1 = '='*Nsmv
str_beg = str_1+'\n\t'+ " программа начала работу"+'\n'+str_1
str_end = str_1+'\n\t'+ " программа закончила работу"+'\n'+str_1
str_tt = str_1+'\n'
name = ''
str_menu = (f'дорогой {name} !!!\nкуда пойдем гулять?\n')
#namеs = {'паша','саша','алексей','антон','федя'}
dict_N = {}
sl = {'дерево','дом'}
#-------Определение функций-------------------------------------------------------------------------------
def Doing_Contin (name, rait):
    print('хорошо '+name+rait)
    print ('Может еще куда-нибудь сходим?\n 0-Завершение работы\n любой символ - продолжение выбора')
    b=input()
    return b
#*********************************************************************************************************
#                                          ОСНОВНОЙ КОД ПРОГРАММЫ
#программа начала работу
namesfl = 'Names.txt'
dict_N = {}
fl = open(namesfl,'r',encoding='UTF-8')
lines=fl.readlines()
fl.close()
print(str_beg)
for l in lines:
    strl=l.strip()
    str3 = strl.split()
    name=str3.pop(0)
    dict_N[name]=str3
namеs = dict_N.keys()
#--------ввод имени------------------------------------
a='1'
while(a!='0'):
    #константы ограничения попыток
    strl = ''
    name = ''
    i = 0
    while((name not in namеs)and(i<imax)):
#----------Авторизация по имени------------------------
        print(str_1)
        print(strl)
        print('как вас зовут?')
        strl= ('имя введено неверно')
        name=input('введите своё имя: ')
        i+=1
    else:
        if((name in namеs) and (i<imax)): # ВСЕ ХОРОШО, ИМЯ ВВЕДЕНО ВЕРНО
            #--------ПРОИЗВЕДЕНИЕ ИНДИФИКАЦИИ ПО ПАРОЛЮ
            print('Привет, '+name+'!!!')
            strl = ''
            i = 0
            pasi = ''
            while((pasi!=dict_N[name][0])and(i<imax)):
                print(strl)
                pasi=input('введите свой пароль: ')
                strl= 'пароль введен не верно'
                i+=1
            else:
                if((pasi == dict_N[name][0]) and (i<imax)): #ВСЁ ХОРОШО, ПАРОЛЬ #№1 ВВЕДЁН ВЕРНО
                    print(''+name+' пароль верный')
                    #-------------------------
                    strl = ''
                    i = 0
                    pasi = ''
                    while((pasi != dict_N[name][1])and(i<imax)):
                        print(str_1)
                        print(strl)
                        pasi=input('Введите следующий пароль: ')
                        strl= 'пароль введен не верно'
                        i+=1
                    else:
                         if((pasi == dict_N[name][1]) and (i<imax)): #ВСЁ ХОРОШО, ПАРОЛЬ #№2 ВВЕДЁН ВЕРНО
                             b='1'
                             print(''+name+' пароль верный')
                             print(str_1)
                             strl = ''
                             i = 0
                             pasi = ''
                             while((pasi != dict_N[name][2])and(i<imax)):
                                     print(strl)
                                     strl= ('Введите следующий пароль')
                                     pasi=input('введите свой пароль: ')
                                     i+=1
                             else:
                                  if((pasi == dict_N[name][2]) and (i<imax)): #ВСЁ СОВСЕМ ХОРОШО, ВСЕ ПАРОЛИ ВВЕДЁНЫ ВЕРНО
                                     b='1'
                                     a='1'
                                     print(''+name+' пароль верный')
                                  else:#ВСЁ ПЛОХО, ПАРОЛЬ №3 ВВЕДЁН НЕ ВЕРНО
                                     b='0'
                                     a='0'
                         else:#ВСЁ ПЛОХО, ПАРОЛЬ №2 ВВЕДЁН НЕ ВЕРНО
                             b='0'
                             a='0'
                else:#ВСЁ ПЛОХО, ПАРОЛЬ  №1 ВВЕДЁН НЕ ВЕРНО
                     b='0'
                     a='0'
        else:#ВСЁ ПЛОХО, ИМЯ ВВЕДЁН0 НЕ ВЕРНО
             b='0'
             a='0'
         #----чтение файла menu.txt----
    check={}
    while(b!='0'):
        Name_fl_menu = 'menu.txt'
        fl = open (Name_fl_menu, 'r', encoding = 'UTF-8')
        Lines = fl.readlines()
        fl.close()
                 #----формирование строки меню----
        str_menu = (f'дорогой {name}\nвыберите товар\n')
        Lines.sort() # сортировка в алфавитном порядке
        s_m = 1
        for L in Lines:
               str1 = L.strip()
               str_menu += f'\t{s_m}) ' + str1.upper()+'\n'
               s_m += 1
        s_m_max = s_m
        str_menu += f'\t{s_m}) ' + 'ничего не покупать\nВвидите номер выбранного меню'
                    #----вывод меню для пользователя на экран----
        print (str_menu)
        num = input()
        #----обработка ответа пользователя----
        test = num.isdigit() # Проверка является ли num числом
        if (test): # все хорошо, num является числом
            num_int = int(num) # преобразование num в целое число
            if ((num_int>0) and (num_int < s_m_max)):
                t1=input('введите количество товара (макс 20): ')
                t=t1.isdigit()#проверка является ли t числом
                #распечатка содержимого heck
                if (t):#всё хорошо t является числом
                    t_int = int(t1)#преоброзование t в целое число
                    if (t_int > 0) and (t_int < 21):#всё хорошо число корректное
                        r1=Lines[num_int-1].strip()
                        r = {}
                        r = r1.split(' ')
                        plays = r.pop(0)
                        r.append(t_int)
                        check[plays]=r
                        print (f'\t ООО,БЕРЛОГА\n телефон: +7(880)-355-55\n почта: berlogaooo@gmail.com\n\t ТОВАРНЫЙ ЧЕК')
                        str1='-'*Nsmv+'\n'
                        str1+='|№|     наиминование      |цена(руб)|кол-во|стоимость|\n'
                        str1+='-'*Nsmv+'\n'
                        keys_L = list(check.keys())
                        keys_L.sort()
                        j=1
                        summ = 0
                        for L in keys_L:
                            cost = float(check[L][0])*int(check[L][1])
                            summ+= cost
                            str1+=f'|{j}|'+ '{:^23}'.format(L)+'|'+'{:^9}'.format(check[L][0])+'|'+'{:^6}'.format(check[L][1])+'|{:^9}|'.format(cost)+'\n'
                            j+=1
                        str1+='-'*Nsmv+'\n'
                        str1+= 'ИТОГО: {:^9}\n'.format(summ)
                        str1+= ("{}.{}.{}  {}:{}".format(now.day, now.month, now.year, now.hour, now.minute))
                        print(str1)
                        print(str_pt)
                        b=input()
                        if b == '0':
                            Namefl_check = (name+ ("{}{}{}_{}{}".format(now.day, now.month, now.year, now.hour, now.minute)) + '.txt')
                            fl=open(Namefl_check,'w',encoding = 'UTF-8')
                            fl.write(f'\t ООО,БЕРЛОГА\n телефон: +7(880)-355-55\n почта: berlogaooo@gmail.com\n\t ТОВАРНЫЙ ЧЕК\n'+str1)
                            fl.close()

#---------------------------------------------------------------------------------------------

                        elif b == '2':
                             keys_L = list(check.keys())
                             keys_L.sort()
                             print('выберите товар который хотите удалить')
                             c=int(input())-1
                             del check [keys_L[c]]
                             print('товар удалён')
                             print(str1)
                             print(str_pt)
                             b=input('')


 # ---------------------------------------------------------------------------------------------




                    elif (num_int ==s_m_max): #ответ при выборе "остаёмся дома"
                        print (f'действие отменено')
                        b='0'
                    else:# все плохо, num не является числом
                        print (f'Дорогой {name} мы вас не поняли\n ввидети корректоное значение ')
                      #-----------------------------------------------------#
            #начать/закончить программу
    if (a != '0'):
        print(str_1)
        print(str_cont)
        a=input()
        print(str_tt)
#программа закончила работу
print(str_end)
