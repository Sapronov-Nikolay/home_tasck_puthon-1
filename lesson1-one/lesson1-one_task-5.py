# Для автоматической перестройки в выводе в терменале кирилицы. Чтобы не → �������, а нормально было.
# Или, если лень, просто запускай в терминале chcp 65001 перед выполнением. 1 раз на сеанс
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ========== ДАЛЕЕ КОД УПРАЖНЕНИЯ ==========

# ЗАДАНИЕ: Параметризация функции.
# ВАРИАНТ 1: Вывод номера в формате без пробелов и знаков 88005553533
def print_num(num):
  print(num, end='')

print()
print("Формат простой без пробелов")
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
print()     # Перевод на новую строку чтобы бвл отступ вниз

# ВАРИАНТ 2: Вывод номера в формате 8 800 555 35 33
def print_with_space(num):
  print(num, end=' ')
def print_no_space(num):
  print(num, end='')

print("Вариант 2: Вывод с пробелами")

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
print_no_space(3)      # последняя 5

# ВАРИАНТ 3: Вывод номера в формате 8 (800) 555-35-33 c str()
print('\nВариант 3: С методом str()')
def str_num(num):
  print(num, end='')

str_num(8)
str_num(str(' (8'))
str_num(0)
str_num(str('0) '))
str_num(5)
str_num(5)
str_num(str('5 '))
str_num(3)
str_num(str('5 '))
str_num(3)
str_num(3)

print()