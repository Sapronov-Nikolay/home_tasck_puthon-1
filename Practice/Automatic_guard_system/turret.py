# Класс Turret управляет турелью: активация, перезарядка, одиночный выстрел, очередь.
# Для звуков используются callback-функция, которая вызывается при каждом выстреле.

import time

class Turret:
    def __init__(self):
        self.is_active = False      # Турель по умолчанию выключена
        self.ammo = 0               # Боезапас пуст
        self.max_ammo = 500         # В обоиме 500 патронов
        self.stop_burst = False     # Флаг для остановки стрельбы

    def activate(self):
        """Включить турель (но патроны могут быть нулевыми)."""
        if not self.is_active:
            self.is_active = True
            print(f"[Турель] Активирована. Патронов: {self.ammo}")
            return True
        else:
            print("[Турель] Уже активна")
            return False

    def deactivate(self):
        """Выключить турель."""
        if self.is_active:
            self.is_active = False
            print("[Турель] Деактивирована")
            return True
        else:
            print("[Турель] Уже не активна")
            return False

    def reload(self):
        """Полностью перезарядить турель (до max_ammo)."""
        self.ammo = self.max_ammo
        print(f"[Турель] Перезаряжена. Патронов: {self.ammo}")
        return True

    def shoot(self):
        """Одиночный выстрел. Возвращает True, если выстрел произведён, иначе False."""
        if not self.is_active:
            print("[Турель] Не активна, стрельба невозможна")
            return False
        if self.ammo > 0:
            self.ammo -= 1
            print(f"[Турель] Выстрел! осталось патронов: {self.ammo}")
            return True
        else:
            print("[Турель] Нет партонов! Перезарядите.")
            return False

    def burst_fire(self, on_shoot_callback=None):
        """
            Стрельба очередью (4 выстрела в секунду).
            on_shoot_callback - функция, которая возвращается при каждом выстреле
            с параметром 'shoot' или 'out_of_ammo' для звука."""
        if not self.is_active:
            print("[Турель] Не активна, стрельба невозможна")
            return
        if self.ammo == 0:
            print("[Турель] Нет патронов! Перезарядите.")
            if on_shoot_callback:
                on_shoot_callback("out_of_ammo")
            return

        self.stop_burst = False
        print("[Турель] Начата стрельба. Нажмите 's' для остановки")
        while self.ammo > 0 and not self.stop_burst:
            if self.shoot():
                if on_shoot_callback:
                    on_shoot_callback("shoot")
            else:
                # Если shoot вернул False (например, патроны кончились), выходим.
                break
            if self.ammo > 0 and not self.stop_burst:
                time.sleep(0.05)    # 5 выстрелов в секунду
        if self.stop_burst:
            print("[Турель] Стрельба остановлена по команде")
        else:
            print("[Турель] Патроны кончились, стрельба завершена")

    def stop(self):
        """Останавливает стрельбу (устанавливаем флаг) Вызывается по нажатию 's'.."""
        print("[Турель] Получена команда остановки!")
        self.stop_burst = True