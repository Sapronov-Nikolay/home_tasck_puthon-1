"""
Программа "Датчик движения с веб-камерой".
Автоматически находит камеру, определяет её разрешение,
размещает зону детекции в центре (квадрат 40% от меньшей стороны).
При движении внутри зоны включает лампу (виртуальную или реальную),
через заданное время без движения выключает.
На экране отображается видео, зелёный прямоугольник зоны,
текстовый статус и цветной индикатор движения.
"""

import cv2
import numpy as np
import time
import threading
from PIL import Image, ImageDraw, ImageFont

# =============================================================================
#  КЛАСС ЛАМПЫ (симуляция)
# =============================================================================
class Lamp:
    """ Управление лампой. Сейчас просто печатаем в консоль
        Для реальной лампы Заменить print на команды управления
    """
    def __init__(self):
        self.is_on = False
        print("Лампа создана (симуляция)")

    def turn_on(self):
        if not self.is_on:
            self.is_on = True
            print("🟡 ЛАМПА ВКЛЮЧЕНА")
            # Здесь будет код включения реальной лампы (serial, GPIO, relay...)

    def turn_off(self):
        if self.is_on:
            self.is_on = False
            print("⚫ ЛАМПА ВЫКЛЮЧЕНА")
            # Здесь код выключения реальной лампы

# =============================================================================
#  ФУНКЦИЯ АВТОМАТИЧЕСКОГО ПОИСКА КАМЕРЫ
# =============================================================================
def find_available_camera(max_test=10):
    """
    Перебирает индексы 0..max_test-1, пытается открыть камеру и захватить кадр.
    Возвращает индекс первой камеры или None.
    """
    print("🔍 Поиск доступной веб-камеры...")
    for i in range(max_test):
        # Параметр cv2.CAP_DSHOW ускоряет открытие камеры в Windows
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"✅ Камера найдена с индексом: {i}")
                cap.release()
                return i
            else:
                print(f"⚠️ Устройство {i} открылось, но не даёт кадр.")
            cap.release()
        print("❌ Работающая камера не найдена.")
        return None

# =============================================================================
#  ОСНОВНОЙ КЛАСС ДАТЧИКА ДВИЖЕНИЯ
# =============================================================================
class MotionSensorCamera:
    """
    Обрабатывает видеопоток, обнаруживает движение в центральной зоне,
    управляет лампой и таймером автовыключения.
    """
    def __init__(self, lamp, timeout=5, sensitivity=25, min_area=500, zone_relative_size=0.4, camera_id=None):
        """
        :param lamp: объект класса Lamp
        :param timeout: секунды без движения до выключения лампы
        :param sensitivity: порог чувствительности (чем меньше, тем выше чувствительность)
        :param min_area: минимальная площадь движения объекта (убирает шум)
        :param zone_relative_size: размер зоны относительно меньшей стороны кадра (0.7 = 70%)
        :param camera_id: индекс камеры (если None, ищетсяавтоматически)
        """
        self.lamp = lamp
        self.timeout = timeout
        self.sensitivity = sensitivity
        self.min_area = min_area
        self.zone_relative_size = zone_relative_size
        self.timer = None
        self.running = True

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
        # Берём меньшую сторону кадра, умножаем на Zone_relative_size
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
        self.prev_grav = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # --- 5. Запускаем отдельный поток для обработки видео ---
        self.thread = threading.Thread(target=self._process)
        self.thread.daemon = True
        self.thread.start()

    def _process(self):
        """Главный цикл обработки кадров (выполняется в отдельном потоке)."""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Ошибка захвата кадра, прерывание процесса...")
                break

            # Текущий кадр в оттенках серого
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Разница между предыдущим кадром и текущим
            diff = cv2.absdiff(self.prev_grav, gray)
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

            # ========== ВИЗУАЛИЗАЦИЯ ==========
            # Рисуем прямоугольник зоны срабатывания (зелёный)
            cv2.rectangle(frame, (self.zone_x, self.zone_y),
                          (self.zone_x + self.zone_w, self.zone_y + self.zone_h), (0, 255, 0), 3)

            # Текст статуса слева вверху
            status_text = "MOTION!!!" if motion_in_zone else "NOT MOTION!!!..."
            color = (0, 255, 0) if motion_in_zone else (0, 255, 0)
            cv2.putText(frame, status_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            # Круг-индикатор в правом верхнем углу
            ind_color = (0, 0, 255) if motion_in_zone else (128, 128, 128)
            circle_x = frame.shape[1] - 30 # Отступ от правого края
            circle_y = 30
            cv2.circle(frame, (circle_x, circle_y), 15, ind_color, -1)
            cv2.circle(frame, (circle_x, circle_y), 15, (255, 255, 255), 2)

            # Если есть движение - дополнительная надпись ВНИМАНИЕ!
            if motion_in_zone:
                cv2.putText(frame, "ALARM!", (circle_x - 110, circle_y + 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            # показываем кадр
            cv2.imshow("Motion Sensor Camera", frame)
            # Проверяем, закрыто ли окно (если окно не существует, завершаем цикл)
            if cv2.getWindowProperty("Motion Sensor Camera", cv2.WND_PROP_VISIBLE) < 1:
                self.stop()
                break
            # Обновляем предыдущий кадр
            self.prev_grav = gray

            # Выход по клавише 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()
                break

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

    # Создаём датчик движения
    # Параметры можно менять: timeout (сек), sensitivity (чувствительность)
    # zone_relative_size (размер зоны в долях от меньшей стороны кадра)
    print("Для выхода нажмите 'q' на латинской раскладке в окне с видео (предварительно кликнув по окну).")
    try:
        sensor = MotionSensorCamera(lamp,
                                    timeout=5,
                                    sensitivity=25,
                                    min_area=500,
                                    zone_relative_size=0.7,
                                    camera_id=None  # None = авто-поиск камеры
                                    )
    except Exception as e:
        print(f"ошибка инициализации: {e}")
        exit(1)

    # Ожидаем завершения (программа работает, пока датчик активен)
    try:
        while sensor.running:
            time.sleep(0.5)
    except KeyboardInterrupt:
        sensor.stop()
        print("Программа заврешена пользователем")