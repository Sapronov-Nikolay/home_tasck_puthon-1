# Для автоматической перестройки в выводе в терменале кирилицы. Чтобы не → �������, а нормально было.
# Или, если лень, просто запускай в терминале chcp 65001 перед выполнением. 1 раз на сеанс
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ========== ДАЛЕЕ КОД УПРАЖНЕНИЯ ==========

# ЗАДАНИЕ: Параметризация функций. Вызвать эту функцию 11 раз
# ВАРИАНТ 1 Выводит 88005553533
def print_num(num):
  print(num, end='')  # По умолчанию функция работы print() имеет параметр " end='\n' " с переносом строки 
                      # и переводит каждый раз новую итерацию на новую строку
                      # Чтобы этого не происходило и номер писался в строчку тужно уирать перенос строки из end

print_num(8)
print_num(8)
print_num(0)
print_num(0)
print_num(5)
print_num(5)
print_num(5)
print_num(3)
print_num(5)
print_num(3)
print_num(3)

print()     # Для перевода курсора в коней чтоб не прилипал к номеру

# ВАРИАНТ 2 Выводит 8 800 555 35 33

def print2_num1(num):
  print(num, end=' ')
print2_num1(8)

def print2_num2(num):
  print(num, end='')
print2_num2(8)
print2_num2(0)

def print2_num3(num):
  print(num, end=' ')
print2_num3(0)

def print2_num4(num):
  print(num, end='')
print2_num4(5)
print2_num4(5)

def print2_num5(num):
  print(num, end=' ')
print2_num5(5)

def print2_num6(num):
  print(num, end='')
print2_num6(3)

def print2_num7(num):
  print(num, end=' ')
print2_num7(5)
def print2_num8(num):
  print(num, end='')
print2_num8(3)
print2_num8(3)

print()     # Для перевода курсора в коней чтоб не прилипал к номеру

# ВАРИАНТ 3 Более короткий и тоже 11 вызовов
def print_with_space(num):
    print(num, end=' ')
def print_no_space(num):
    print(num, end='')

print("Вариант 3 (с пробелами):")
print_with_space(8)    # 8 + пробел
print_no_space(8)      # 8
print_no_space(0)      # 0
print_with_space(0)    # 0 + пробел
print_no_space(5)      # 5
print_no_space(5)      # 5
print_with_space(5)    # 5 + пробел
print_no_space(3)      # 3
print_with_space(5)    # 5 + пробел
print_no_space(3)      # 3
print_no_space(5)      # последняя 5
print()   # перевод строки