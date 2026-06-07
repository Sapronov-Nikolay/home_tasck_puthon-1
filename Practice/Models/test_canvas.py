import tkinter as tk

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Pillow не установлен. Картинки недоступны.")

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Matplotlib не установлен. Графики недоступны.")
#=====================================================================================

# Создаём окно и холст (достаточно большой)
def main():
    root = tk.Tk()
    root.title("Тестовое поле для просмотра элементов графики")
    root.geometry("1024x900")  # окно чуть больше холста, чтобы видеть кнопку

    # Кнопка для очистки холста (удобно)
    def clean_canvas():
        canvas.delete('all')
        # Отрисовываем заново сетку
        for i in range(0, 1000, 50):
            canvas.create_line(i, 0, i, 800, fill='#8aabdb')  # Вертикаль
            canvas.create_line(0, i, 1000, i, fill='#8aabdb')  # Горизонталь

    btn = tk.Button(root, text="Очистить поле", command=clean_canvas)
    btn.pack(pady=5)

    # Холст (1000x800, чтобы влез в экран)
    canvas = tk.Canvas(root, width=1000, height=800, bg='#efe9cd')
    canvas.pack()

    # Сетку после очистки заново фоновая
    for i in range(0, 1000, 50):
        canvas.create_line(i, 0, i, 800, fill='#8aabdb')   # Вертикаль
        canvas.create_line(0, i, 1000, i, fill='#8aabdb')   # Горизонталь


    # ============================================
    # СЮДА ВСТАВЛЯЙТЕ ЛЮБЫЕ КОМАНДЫ РИСОВАНИЯ
    # ============================================
    # Пример из другого проекта:
    # Можно добавить сюда что угодно:
    # canvas.create_rectangle(10, 10, 90, 90, fill='red')
    # canvas.create_line(0, 0, 200, 200, width=3)
    # --------------------------------------------
    canvas.create_oval(40, 30, 160, 110, fill='gray', outline='black')


    # ============================================
    # Зона запуска программы

    root.mainloop()
if __name__ == '__main__':
    main()