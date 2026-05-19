# ЗАДАНИЕ: Задачка с собеседования "Fizz/Buzz"
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