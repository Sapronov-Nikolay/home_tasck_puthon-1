import tkinter as tk # Импортируем библиотеку Tkinter для GUI
import math # Импортируем модуль math для математических вычислений

class Person:
    """
    Класс, представляющий синий квадратик, который будет следовать за курсором или перетаскиваться
    """
    def __init__(self, canvas, x=50, y=50):
        """
        Инициализация квадратика.
        :param canvas: холст (объект tk.Canvas), на котором рисуется квадратик
        :param x, y: начальные координаты центра квадратика
        """
        self.canvas = canvas
        # Рисуем синий квадратик 30х30. Метод create_rectangle() возвращает уникальный ID фигуры
        self.id = canvas.create_rectangle(0, 0, 30, 30, fill='blue')
        # Перемещаем квадратик в заданную начальную позицию
        self.move_to(x, y)

    def move_to(self, x, y):
        """
        Перемещает квадратик так, чтобы его центр оказался в точке (x, y).
        :param x: Координата x центра
        :param y: Координата y центра
        """
        self.x = x  # Запоминаем текущую координату X центра
        self.y = y  # Запоминаем текущую координату Y центра
        # Метод coords() изменяет похожие фигуры на холсте
        # Квадрат 30х30, поэтому верхний левый угол будет в (x-15, y-15), нижний правый - в (x+15, y+15)
        # По сути мы делим квадратный диаметр попалам - на радиусы, чтобы позиционировать его центр, а не края.
        self.canvas.coords(self.id, x - 15, y - 15, x + 15, y + 15)


class Lamp:
    """Класс, представляющий лампу - круг, могущий быть включён (жёлтый) или выключен (серый)."""
    def __init__(self, canvas, x, y):
        """
        Инициализация лампы.
        :param canvas: холст для рисования
        :param x, y: координаты центра круга
        """
        self.canvas = canvas # Сохраняем ссылку на холст
        # Рисуем серый круг диаметром 50 пикс (радиус 25 пикс)
        self.id = canvas.create_oval(x - 25, y - 25, x + 25, y + 25, fill='gray', outline='black')
        self.is_on = False # Изначально лампа выключена

    def turn_on(self):
        """Включает лампу (меняет цвет на жёлтый и устанавливает флаг is_on со значением True"""
        self.canvas.itemconfig(self.id, fill='yellow')  # Меняем заливку круга - включено
        self.is_on = True

    def turn_off(self):
        """Выключает лампу (меняет цвет с жёлтого на серый и сбрасывает флаг is_on (False)"""
        self.canvas.itemconfig(self.id, fill='gray') # Возвращаем серый цвет круга - выключено
        self.is_on = False


class MotionSensor:
    """
    Класс датчика движения.
    Постоянно проверяет расстояние от синего квадратика Person до центра датчика MotionSensor.
    Если синий квадратик в зоне действия - включает лампу и запускает таймер на отключение
    Лампа выключится через 5 секунд после последнего входа в зону.
    """
    def __init__(self, canvas, person, lamp, sensor_x, sensor_y, radius=60):
        """
        Инициализация датчика.
        :param canvas: это холст
        :param person: это объект экземпляра класса Person (синий квадратик)
        :param lamp: это объект экземпляра класса Lamp (лампа)
        :param sensor_x, sensor_y: это координаты центра зоны датчика
        :param radius: это радиус зоны обнаружения (по умолчанию 60 → можно установить любую)
        """
        self.canvas = canvas    # Ссылка на холст
        self.person = person    # Cсылка на объект "синий квадратик"
        self.lamp = lamp        # Ссылка на объект лампа
        self.sensor_x = sensor_x    # Ссылка на координаты центра датчика по оси X
        self.sensor_y = sensor_y    # Ссылка на координаты центра датчика по оси Y
        self.radius = radius    # Ссылка на радиус зоны действия датчика
        self.timer = None       # Ссылка для ID таймера (для отмены)
        self.last_x = person.x  # Ссылка для запоминания позиции по оси X
        self.last_y = person.y  # Ссылка для запоминания позиции по оси Y
        # Рисуем пунктирную окружность - зону действия датчика
        self.sensor_id = canvas.create_oval(
            sensor_x - radius, sensor_y - radius, sensor_x + radius, sensor_y + radius,
            outline='#575341', dash=(8, 5), width=2 # dash создаёт пунктирную линию
        )
        # Запускаем бесконечную проверку положения синего квадратика
        self.check()

    def check(self):
        """Проверяет расстояние до синего квадратика и его движение и управляет лампой"""
        # Вычисляем разницу координат между центром датчика и центром синего квадратика
        dx = self.sensor_x - self.person.x
        dy = self.sensor_y - self.person.y
        # Формула расстояния между двумя точками (теорема Пифагора)
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Проверяем, двигается ли квадратик
        moved = (abs(self.person.x - self.last_x) > 1 or
                 abs(self.person.y - self.last_y) > 1)
        self.last_x = self.person.x
        self.last_y = self.person.y

        if distance <= self.radius and moved:
            # Человек внутри или коснулся зоны: включаем лампу
            self.lamp.turn_on()
            # Если таймер уже установлен - отменяем его
            if self.timer:
                self.canvas.after_cancel(self.timer) # after_cancel отменяет отложенный вызов
            # Запускаем новый таймер: через 5000 мс (5 сек) лампа выключится
            self.timer = self.canvas.after(5000, self.lamp.turn_off)
        # Планируем следующий вызов check() через 100 мс (0,1 сек)
        # Это создаёт "цикл" проверки положения
        self.canvas.after(100, self.check)


class App:
    def __init__(self, root):
        """
        Главный класс приложения.
        Создаёт окно, холст, объекты и связывает события.
        :param root: корневое окно Tkinter
        """
        self.root = root
        root.title("Датчик движения - режим следования за курсором/перетаскивания") # Устанавливаем заголовок окна

        # Рассчитываем размер и позицию окна для центрирования
        w, h = 600, 400     # Ширина и высота окна
        ws = root.winfo_screenwidth()   # Ширина экрана
        hs = root.winfo_screenheight()  # высота экрана
        x = (ws - w) // 2  # Горизонтальная позиция для центрирования
        y = (hs - h) // 2  # Вертикальная позиция для центрирования
        root.geometry(f"{w}x{h}+{x}+{y}")   # Устанавливаем размер и позицию окна

        # Создаём фрейм для кнопки управления режимом
        control_frame = tk.Frame(root)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        # Кнопка переключения режима
        self.mode_button = tk.Button(
            control_frame,
            text="Режим: Следование за курсором",
            command=self.toggle_mode
        )
        self.mode_button.pack(pady=5)

        # Создаём холст (комнату) с серым фоном
        self.canvas = tk.Canvas(root, width=w, height=h, bg='lightgray')
        self.canvas.pack()

        # Создаём объекты: синий квадратик, лампа, датчик
        self.person = Person(self.canvas, 100, 100) # Квадратик стартует в (100, 100)
        self.target_x = self.person.x
        self.target_y = self.person.y
        self.grag_mode = False
        self.dragging = False # Флаг: перетаскивание (активно оно или нет)
        self.offset_x = 0   # Смещение по X от центра объекта до курсора
        self.offset_y = 0   # Смещение по Y от центра объекта до курсора
        self.animate()
        self.lamp = Lamp(self.canvas, 300, 200) # Лампа в (300, 200)
        # Датчик: центр в (150, 150), радиус 80
        self.sensor = MotionSensor(self.canvas, self.person, self.lamp, 150, 150, radius=80)
        # Флаг режима: True - перетаскивание, False - следование за курсором
        # Привязываем события в зависимости от режима
        self.setup_bindings()

    def setup_bindings(self):
        """Настраивает привязки событий в зависимости от текущего режима."""
        # Убираем все предыдущие привязки
        self.canvas.unbind('<Motion>')
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')

        if self.grag_mode:
            # Режим перетаскивания: приаязываем события мыши для drag-and-drop
            self.canvas.bind('<Button-1>', self.on_mouse_press) # Нажатие левой кнопкой мыши
            self.canvas.bind('<B1-Motion>', self.on_mouse_drag) # Движение с зажатой кнопкой
            self.canvas.bind('<ButtonRelease-1>', self.on_mouse_release) # Отпускание кнопки
        else:
            # Кужим следования за курсором: привязываем движение мыши
            self.canvas.bind('<Motion>', self.on_mouse_move) # Следование за курсором мыши

    def toggle_mode(self):
        """Переключает режим между следованием за курсором и перетаскиванием."""
        self.grag_mode = not self.grag_mode # Меняем режим на противоположный
        # Обновляем текст на кнопке
        if self.grag_mode:
            self.mode_button.config(text="Режим: Перетаскивание")
        else:
            self.mode_button.config(text="Режим: Следование за курсором")
        # перенастраиваем привязки событий
        self.setup_bindings()

    def on_mouse_press(self, event):
        """Обработчик нажатия левой кнопки мыши - проверяет, попал ли курсор в объект."""
        x, y = event.x, event.y
        person = self.person
        # Координаты углов квадратика (30х30, центр в person.x, person.y)
        x1, y1 = person.x - 15, person.y - 15 # Верхний левый угол
        x2, y2 = person.x + 15, person.y + 15 # Нижний правый угол

        # Проверяем, находится ли курсор внутри квадратика
        if x1 <= x <= x2 and y1 <= y <= y2:
            self.dragging = True
            self.offset_x = person.x - x
            self.offset_y = person.y - y

    def on_mouse_drag(self, event):
        """Обработчик движения мыши с зажатой клавишей - перемещает объект"""
        if self.dragging:
            x, y = event.x, event.y
            # Вычисляем новую позицию центра объекта
            # Вычисляем сохранённое смещение, чтобы курсор оставался в той же точке смещения
            new_x = x + self.offset_x
            new_y = y + self.offset_y
            # Перемещаем объект в новую позицию
            self.person.move_to(new_x, new_y)

    def on_mouse_release(self, event):
        """Обработчик отпускания левойкнопки мыши - завершает перетаскивание."""
        self.dragging = False
        # Сбрасываем смещение - на случай следующего перетаскивания
        self.offset_x = 0
        self.offset_y = 0

    def on_mouse_move(self, event):
        """
        Обработчик движения мыши.
        Просто запоминаем позицию курсора, куда нужно двигаться.
        """
        # Вместо мгновенного следования за курсором - двигаемся с 40%-ым отставанием
        self.target_x = event.x
        self.target_y = event.y

    def animate(self):
        """Постоянно подтягивает синий квадратик к целевой точке (курсору)."""
        if not self.grag_mode: # Только в режиме следования
            dx = self.target_x - self.person.x
            dy = self.target_y - self.person.y
            if abs(dx) > 1 or abs(dy) > 1:
                self.person.move_to(self.person.x + dx * 0.15,
                                    self.person.y + dy * 0.15)
        self.root.after(30, self.animate)

# Запускаем окно по требованию пользователя, чтоб весь файл запустился, а не отработал в терминале
if __name__ == '__main__':
    # Создаём корневое окно Tkinter
    root = tk.Tk()
    # Создаём экземпляр класса приложения
    app = App(root)
    # Запускаем главный цикл обработки событий
    root.mainloop()