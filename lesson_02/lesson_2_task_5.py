# Для автоматической перестройки в выводе в терменале кирилицы. Чтобы не → �������, а нормально было.
# Или, если лень, просто запускай в терминале chcp 65001 перед выполнением. 1 раз на сеанс
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ========== ДАЛЕЕ КОД УПРАЖНЕНИЯ ==========

# ЗАДАНИЕ: Месяц - сезон
# ВАРИАНТ 1
def month_to_season(month):
  if month in (12, 1, 2):
    return "Зима"
  elif month in (3, 4, 5):
    return "Весна"
  elif month in (6, 7, 8):
    return "Лето"
  elif month in (9, 10, 11):
    return "Осень"
  else:
    return "Введён неверный номер месяца"
  
print(month_to_season(2))

# ВАРИАНТ 2 С input продолжение варианта без начала функции... она из первоно варианта...
try:
  user_input = int(input("Введите номер месяца (1-12): "))
  season = month_to_season(user_input)
  print(f"Месяц {user_input} относится к сезону: {season}")
except ValueError:
  print("Ошибка! Введите целое число.")

# ВАРИАНТ 3 Через список.
def month_to_season_list(month):
  seasons = ["", "Зима", "Зима", "Весна", "Весна", "Весна", "Лето", "Лето", "Лето", "Осень", "Осень", "Осень", "Зима"]
  if 1 <= month <= 12:
    return seasons[month]
  return "Неверный номер месяца"
try:
  user_input = int(input("Введите номер месяца (1-12): "))
  season = month_to_season_list(user_input)
  print(f"Месяц {user_input} относится ксезону: {season}")
except ValueError:
  print("Ошибка! Введите целое число")