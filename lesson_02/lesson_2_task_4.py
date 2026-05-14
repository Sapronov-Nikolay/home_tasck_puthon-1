# Для автоматической перестройки в выводе в терменале кирилицы. Чтобы не → �������, а нормально было.
# Или, если лень, просто запускай в терминале chcp 65001 перед выполнением. 1 раз на сеанс
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ========== ДАЛЕЕ КОД УПРАЖНЕНИЯ ==========

# ЗАДАНИЕ: Задачка с собеседования "Fizz/Buzz"
# ВАРИАНТ 1
def fizz_buzz(n):
  for i in range(1, n + 1):
    # Сначала идёт составное условие, иначе до него очередь не дойдёт.
    if i % 3 == 0 and i % 5 == 0:
      print("FizzBuzz", end=" ")
    elif i % 3 == 0:
      print("Fizz", end=" ")
    elif i % 5 == 0:
      print("Buzz", end=" ")
    else:
      print(i, end=" ")

# Вызываемся
fizz_buzz(17)

# ВАРИАНТ 2
def fizz_buzz(n):
  for i in range(1, n + 1):
    print("fizz" * (i % 3 == 0) + "Buzz" * (i % 5 == 0) or i)

# Вызываемся
fizz_buzz(17)