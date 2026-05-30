"""
Программа "Датчик движения с веб-камерой".
Автоматически находит камеру, определяет её разрешение,
размещает зону детекции в центре (прямоугольник 70% от кадра).
При движении внутри зоны включает лампу (виртуальную или реальную),
через заданное время без движения выключает.
На экране отображается видео, зелёный прямоугольник зоны,
текстовый статус и цветной индикатор движения.
Поддерживает русский и английский язык текста на кадре камеры.
Окно можно развернуть на весь экран (клавиша F) - видео растягивается с сохранением пропорций.
"""

import cv2
import numpy as np
import time
import os
import threading
from PIL import Image, ImageDraw, ImageFont # Для вывода русского текста

# =============================================================================
#  КЛАСС ЛАМПЫ (симуляция)
# =============================================================================
class Lamp:
    """ Управление лампой. Сейчас просто печатаем в консоль"""
    def __init__(self):
        self.is_on = False
        print("Лампа создана (симуляция)")

    def turn_on(self):
        if not self.is_on:
            self.is_on = True
            print("🟡 ЛАМПА ВКЛЮЧЕНА")

    def turn_off(self):
        if self.is_on:
            self.is_on = False
            print("⚫ ЛАМПА ВЫКЛЮЧЕНА")

# =============================================================================
#  ФУНКЦИЯ АВТОМАТИЧЕСКОГО ПОИСКА КАМЕРЫ
# =============================================================================
def find_available_camera(max_test=10, warnum_delay=0.1):
    """
    Перебирает индексы 0..max_test-1, пытается открыть камеру и захватить кадр.
    Возвращает индекс первой камеры или None.
    warmup_delay - задержка (сек) для инициализации камеры.
    """
    print("🔍 Поиск доступной веб-камеры...")
    backend = cv2.CAP_DSHOW if os.name == 'nt' else 0
    for i in range(max_test):
        # Параметр cv2.CAP_DSHOW ускоряет открытие камеры в Windows
        cap = cv2.VideoCapture(i, backend)
        time.sleep(warnum_delay)    # Даём камере время "проснуться"и откликнуться на запрос
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"✅ Камера найдена с индексом: {i}")
                cap.release()
                return i
            else:
                print(f"⚠️ Устройство {i} открылось, но не даёт кадр.")
        else:
            print(f"❌ Камера с индексом {i} не найдена.")
        cap.release()   # Освобождаем в любом случае
    print("❌ Работающая камера не найдена.")
    return None

# =============================================================================
#  УНИВЕРСАЛЬНАЯ ФУНКЦИЯ ДЛЯ ВЫВОДА ТЕКСТА (русский + английский)
# =============================================================================
def put_text(frame, text, position, font_size=24, color=(0, 0, 255), thickness=2):
    """
    Универсальная функция для вывода текста на кадр.
    Если в тексте есть кириллица - использует Pilliw (медленнее, но поддерживает русский).
    Если текст на латинице - использует cv2.putText (быстрее).
    Параметры:
        :param frame: кадр OpenCV (numpy array)
        :param text: текст для вывода (русский или английский)
        :param position: кортеж (x, y) - координаты левого нижнего угла текста
        :param font_size: размер шрифта в пикселях (для русского - точный, для английского - приблизительный)
        :param color: цвет в формате BGR (синий-зелёный-красный), например (0, 0, 255) - красный
        :param thickness: толщина линии (только для английского, для русского не используется)
    """
    # Проверяем, есть ли в тексте русские буквы (диапазон Unicode кириллицы)
    has_cyrillic = any('\u0400' <= char <= '\u04FF' for char in text)

    if has_cyrillic:
        # ========== РУССКИЙ ТЕКСТ через Pillow ==========
        # Конвертируем кадр из BRG (OpenCV) в RGB (Pillow)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pill_img = Image.fromarray(frame_rgb)
        draw = ImageDraw.Draw(pill_img)

        # Загружаем шрифт, поддерживающий кириллицу
        try:
            # Пробуем загрузить Arial (стандартный шрифт Windows)
            font = ImageFont.truetype("arial.ttf", font_size)
        except OSError:
            try:
                # Альтернативный путь для Windows
                font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", font_size)
            except OSError:
                # Запасной вариант: используем дефолтный шрифт от Pillow (не поддерживает кириллицу, но не падает)
                font = ImageFont.load_default()

        # преобразуем BGR -> RGB
        color_rgb = (color[2], color[1], color[0])
        draw.text(position, text, font=font, fill=color_rgb)    # color уже в RGB? Нет, OpenCV использует BRG
        # Важно: draw.text ожидает RGB, но мы передаём BRG - цвета будут неправильные.
        # Для корректного цвета нужно преобразовать, но для простоты оставим как есть.
        # Правильно: color_rgb = (color[2], color[1], color[0]) - но это уже тонкости.

        # Конвертируем обратно в RGB для OpenCV
        frame_bgr = cv2.cvtColor(np.array(pill_img), cv2.COLOR_RGB2BGR)
        return frame_bgr
    else:
        # ========== АНГЛИЙСКИЙ ТЕКСТ через cv2.putText (быстро) ==========
        # Масштаб шрифта: font_size / 20 - эмпирическая формула для совместимости размера
        scale = font_size / 20
        cv2.putText(frame, text, position, cv2.FONT_HERSHEY_PLAIN, scale, color, thickness)
        return frame

# =============================================================================
#  ФУНКЦИЯ МАСШТАБИРОВАНИЯ КАДРА С СОХРАНЕНИЕМ ПРОПОРЦИЙ
# =============================================================================
def resize_frame_keep_aspect_with_offset(frame, target_width, target_height):
    """
    Масштабирует кадр с сохренением пропорций, центрирует по полям.
    Возвращает новый кадр размером target_width x target_height с чёрными полями по бокам
    Работает как на уменьшение, так и на увличение контейнера
    """
    h, w = frame.shape[:2]  # Исходная ширина и высота
    # Вычисляем коэфицент масштабирования, чтобы кадр вписался в целое окно
    scale = min(target_width / w, target_height / h)
    new_w = int(w * scale)  # новая ширина по ширине после масштабирования
    new_h = int(h * scale)  # новая ширина по высоте после масштабирования
    # Выбираем интерполяцию: при уменьшении - AREA, при увеличении - CUBIC
    interpolation = cv2.INTER_AREA if scale < 1 else cv2.INTER_CUBIC
    resized = cv2.resize(frame, (new_w, new_h), interpolation=interpolation)

    # Создаём чёрное полотно целевого размера
    result = np.zeros((target_height, target_width, 3), dtype=np.uint8)

    # Вычисляем отступы для центрования
    x_offset = (target_width - new_w) // 2
    y_offset = (target_height - new_h) // 2

    # Выставляем масштабированный кадр в центр
    result[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = resized
    return result, x_offset, y_offset, new_w, new_h

# =============================================================================
#  ОСНОВНОЙ КЛАСС ДАТЧИКА ДВИЖЕНИЯ
# =============================================================================
class MotionSensorCamera:
    """
    Обрабатывает видеопоток, обнаруживает движение в центральной зоне,
    управляет лампой и таймером автовыключения.
    Вся обработка и отображение происходят в главном потоке (без threading).
    """
    def __init__(self, lamp, timeout=5, sensitivity=25, min_area=500, zone_relative_size=0.7, window_width=1024, window_height=768, camera_id=None):
        """
        :param lamp: объект класса Lamp
        :param timeout: секунды без движения до выключения лампы
        :param sensitivity: порог чувствительности (чем меньше, тем выше чувствительность)
        :param min_area: минимальная площадь движения объекта (убирает шум)
        :param zone_relative_size: размер зоны относительно меньшей стороны кадра (0.7 = 70%)
        :param window_width: начальная ширина окна
        :param window_height: начальная высота окна
        :param camera_id: индекс камеры (если None, ищетсяавтоматически)
        """
        self.lamp = lamp
        self.timeout = timeout
        self.sensitivity = sensitivity
        self.min_area = min_area
        self.zone_relative_size = zone_relative_size
        self.window_width = window_width
        self.window_height = window_height

        # --- 1. Находим камеру ---
        if camera_id is None:
            camera_id = find_available_camera()
            if camera_id is None:
                raise RuntimeError("Не удалось найти камеру.")
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(self.camera_id, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            raise IOError(f"Не удалось открыть камеру {self.camera_id}")

        # --- 2. Определяем реальное разрешение кадров ---
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Разрешение камеры: {self.frame_width}x{self.frame_height}")

        # --- 3. Вычисляем зону интереса (зону срабатывания - центральный квадрат) ---
        # Берём меньшую сторону кадра, умножаем на zone_relative_size
        side = int(min(self.frame_width, self.frame_height) * self.zone_relative_size)
        self.zone_w = side
        self.zone_h = side
        self.zone_x = (self.frame_width - self.zone_w) // 2
        self.zone_y = (self.frame_height - self.zone_h) // 2
        print(f"Зона зона срабатывания: x={self.zone_x}, y={self.zone_y}, w={self.zone_w}, h={self.zone_h}")

        # --- 4. Захватываем первый кадр для инициализации фона ---
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Не удалось захватить первый кадр")
        self.prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # --- 5. Создаём окно с возможностью изменения размера ---
        self.window_name = "Motion Sensor Camera"
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, self.window_width, self.window_height)
        self.fullscreen = False
        self.running = True
        self.timer = None

    def _process(self):
        """Главный цикл обработки кадров (выполняется в отдельном потоке)."""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Ошибка захвата кадра, прерывание процесса...")
                break

            # ---------- Обработка движения ----------
            # Текущий кадр в оттенках серого
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Разница между предыдущим кадром и текущим
            diff = cv2.absdiff(self.prev_gray, gray)
            # Пороговая обработка (пиксели, изменившиеся сильнее порога)
            _, thresh = cv2.threshold(diff, self.sensitivity, 255, cv2.THRESH_BINARY)
            # Поиск контуров (областей изменений)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Флаг - есть ли срабатывание внутри зоны
            motion_in_zone = False
            # перебираем все найденные контуры
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area < self.min_area:
                    continue    # Игнорируем мелкие шумы
                # Вычисляем центр контура
                M = cv2.moments(cnt)
                if M["m00"] == 0:
                    continue
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                # Проверка попадания центра в зону
                left = self.zone_x
                right = self.zone_x + self.zone_w
                top = self.zone_y
                bottom = self.zone_y + self.zone_h
                if (left <= cx <= right) and (top <= cy <= bottom):
                    motion_in_zone = True
                    break

            # Управление лампой (включение и таймер выключения)
            if motion_in_zone:
                self.lamp.turn_on()
                if self.timer is not None:
                    self.timer.cancel()
                self.timer = threading.Timer(self.timeout, self.lamp.turn_off)
                self.timer.start()
            # Если движения нет - ничего не делаем, таймер сам выключит лампу

            # ========== ВИЗУАЛИЗАЦИЯ С МАСШТАБИРОВАНИЕМ ==========
            # 1. Получаем текущий размер окна (для динамического масштабирования)
            # Визуализация с фиксированным размером окна
            #display_frame = resize_frame_keep_aspect(frame, self.window_width, self.window_height)
            try:
                rect = cv2.getWindowImageRect(self.window_name)
                if rect is not None and rect[2] > 0 and rect[3] > 0:
                    curr_width = rect[2]
                    curr_height = rect[3]
                else:
                    curr_width = self.window_width
                    curr_height = self.window_height
            except:
                curr_width = self.window_width
                curr_height = self.window_height

            # Масштабируем кадр с сохранением пропорций
            display_frame, x_offset, y_offset, new_w, new_h = resize_frame_keep_aspect_with_offset(
                frame, curr_width, curr_height)

            # 2. Рисуем прямоугольник зоны срабатывания (зелёный)
            # Пересчитываем координаты зоны с учётом отступов
            zone_x1 = int(self.zone_x * (new_w / self.frame_width)) + x_offset
            zone_y1 = int(self.zone_y * (new_h / self.frame_height)) + y_offset
            zone_x2 = int((self.zone_x + self.zone_w) * (new_w / self.frame_width)) + x_offset
            zone_y2 = int((self.zone_y + self.zone_h) * (new_h / self.frame_height)) + y_offset
            cv2.rectangle(display_frame, (zone_x1, zone_y1), (zone_x2, zone_y2), (0, 255, 0), 3)

            # 3. Текст статуса слева вверх
            status_text = "ДВИЖЕНИЕ!!!" if motion_in_zone else "НЕТ ДВИЖЕНИЯ..."
            text_color = (0, 0, 255) if motion_in_zone else (0, 255, 0) # красный / зелёный
            display_frame = put_text(display_frame, status_text, (20, 25),
                                     font_size=32, color=text_color, thickness=2)

            # 4. Круг-индикатор в правом верхнем углу
            ind_color = (0, 0, 255) if motion_in_zone else (128, 128, 128)
            circle_x = curr_width - 40 # Отступ от правого края
            circle_y = 40
            cv2.circle(display_frame, (circle_x, circle_y), 20, ind_color, -1)
            cv2.circle(display_frame, (circle_x, circle_y), 20, (255, 255, 255), 2)

            # 5. Если есть движение - дополнительная надпись ВНИМАНИЕ!
            if motion_in_zone:
                display_frame = put_text(display_frame, "ВНИМАНИЕ!", (circle_x - 230, circle_y - 15),
                                         font_size=32, color=(0, 0, 255), thickness=2)
            cv2.imshow(self.window_name, display_frame)

            # обработка клавиш
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                self.stop()
                break
            elif key == ord("f"):
                # Переключение полноэкранного режима
                self.fullscreen = not self.fullscreen
                if self.fullscreen:
                    cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                else:
                    cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
                    cv2.resizeWindow(self.window_name, self.window_width, self.window_height)

            # Проверка, закрыто ли окно крестиком с помощью мыши
            if cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1:
                self.stop()
                break
            # В конце цикла обновляем предыдущий кадр
            self.prev_gray = gray

    def stop(self):
        """Останавливает захват видео и закрывает окна."""
        self.running = False
        if self.timer:
            self.timer.cancel()
        if hasattr(self, "cap") and self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Датчик движения остановлен.")

# =============================================================================
#  ЗАПУСК ПРОГРАММЫ
# =============================================================================
if __name__ == "__main__":
    # Создаём лампу (виртуальную)
    lamp = Lamp()
    print("Управление:")
    print(" • 'q' - Выход")
    print(" • 'f' - полноэкранный режим / окно")
    print(" • Можно растягивать окно за края - видео подстроится")
    print(" • Для работы детекции зона считается на исходном кадре, но прямоугольник может быть немного смещён"
          "при масштабировании. Это не влияет на определение движения")
    print("Для выхода нажмите 'q' на латинской раскладке в окне с видео (предварительно кликнув по окну).")


    # Создаём датчик движения
    # Параметры можно менять: timeout (сек), sensitivity (чувствительность)
    # zone_relative_size (размер зоны в долях от меньшей стороны кадра)
    try:
        sensor = MotionSensorCamera(lamp,
                                    timeout=5,
                                    sensitivity=25,
                                    min_area=500,
                                    zone_relative_size=0.7,
                                    window_width=1024,
                                    window_height=768,
                                    camera_id=None  # None = авто-поиск камеры
                                    )
        sensor._process()
    except Exception as e:
        print(f"ошибка инициализации: {e}")
        exit(1)