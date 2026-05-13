# Для автоматической перестройки в выводе в терменале кирилицы. Чтобы не → �������, а нормально было.
# Или, если лень, просто запускай в терминале chcp 65001 перед выполнением. 1 раз на сеанс
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ========== ДАЛЕЕ КОД УПРАЖНЕНИЯ ==========

# ЗАДАНИЕ: Площадь квадрата
# ВАРИАНТ 1
import math

def square(side):
  """
  Вычисляет площадь квадрата.
  Если аргумент не целое число, то округляет результат вверх.
  """
  area = side * side # Вычисляем площадь
  if not isinstance(side, int): # Если сторона не целое число
    return math.ceil(area)  # Округляем вверх если not isinstance() подтверждено
  return area # Возвращаем обычное число

# Выводим стороны вдвух вариантах
print(square(5))    # → Выведет 25 (целое число, округлять нет нужды)
print(square(2.3))  # → Выведет 6 (2,3 * 2,3 = 5,29 → отсекает дробную часть прибавляя 1)

# ВАРИАНТ 2
def square(side):
  area = side * side
  if not isinstance(side, int):
    return math.ceil(area)
  return area

# Пишем код для ввода сторон квадрата пользователем
try:
  side = float(input("Введите длину стороны квадрата:\n"))
  result = square(side)
  print(f"Площадь квадрата: {result}")
except ValueError:
  print("Ошибка! Введите число, например: 5 или 2.5")

# ВАРИАНТ 3: С тремя попытками ввести сторону, если вводится не число.
print("\nВариант 3: В случае неверного ввода будет дано ещё 2 попытки")
def square(side):
  area = side * side
  if not isinstance(side, int):
    return math.ceil(area)
  return area

# Пишем код для ввода сторон квадрата.
try:
  side = float(input("Введите длину стороны квадрата, например: 5 или 2.5:\n"))
  result = square(side)
  print(f"Площадь квадрата: {result}")
except ValueError:
  # Если ошибка - запускаем цикл с двумя попытками ввода
  max_attempts = 2
  while max_attempts > 0:
    # Формируем сообщение с правильным склонением
    if max_attempts == 1:
      message = f"Ошибка! У вас осталась {max_attempts} попытка."
    else:
      message = f"Ошибка! У вас осталось {max_attempts} попытки."
    print(message)

    try:
      side = float(input("Попробуйте ввести число, например: 5 или 2.5:\n"))
      result = square(side)
      print(f"Площадь квадрата: {result}")
      break # Успешно - выходим из цикла
    except ValueError:
      max_attempts -= 1
  else:
    # Все попытки исчерпаны
    print("Сожалеем, что вы так и не смогли ввести данные. Спасибо!")