# 1. Создайте файл lesson_3_task_1.py.
# 2. Импортируйте в него класс User из файла user.py.
from user import User

# 3. Создайте новый экземпляр User и сохраните его в переменную my_user.
my_user = User("Николай", "Сапронов")

# 5. Вызовите все методы у объекта в переменной my_user.
print("Вывод имени: ")
my_user.print_first_name()

print("Вывод фамилии: ")
my_user.print_last_name()

print("Вывод имени и фамилии: ")
my_user.print_full_name()