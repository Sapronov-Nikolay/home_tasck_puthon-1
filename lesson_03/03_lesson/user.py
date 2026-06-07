# 1. Создайте файл user.py.
# 2. В файле объявите класс User.
class User:
# 3. Объявите в классе конструктор.
    def __init__(self, first_name, last_name):
# Конструктор должен принимать на вход два параметра:
# first_name — имя;
# last_name — фамилия.
        self.first_name = first_name
        self.last_name = last_name
#
# 4. Создайте в классе три метода, которые печатают: имя, фамилию, имя и фамилию.
    def print_first_name(self):
        print(self.first_name)

    def print_last_name(self):
        print(self.last_name)

    def print_full_name(self):
        print(self.first_name + ' ' + self.last_name)