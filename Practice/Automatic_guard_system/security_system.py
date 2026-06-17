# security_system.py
import time
import threading
import keyboard
from door import Door
from turret import Turret
from sound_manager import SoundManager

class SecuritySystem:
    """
        Главный класс, который связывает все компоненты:
        - дверь (Door)
        - турель (Turret)
        - звуки (SoundManager)
        - управление с клавиатуры (горячие клавиши)
        - паузу (отключение управления)
        - установку произвольного количества патронов через ввод числа
    """
    def __init__(self, sound_manager):
        # Создаём объекты двери и турели
        self.door = Door()
        self.turret = Turret()
        # Сохраняем менеджер звуков для воспроизведения
        self.sound_manager = sound_manager
        # Флаг работы программы (используется в цикле)
        self.running = True
        # Флаг управления: True - клавиши работают, False - игнорируются (пауза)
        self.control_enabled = True
        # Список для хранения идентификаторов для клавиш,
        # чтобы можно было их отключать и восстанавливать
        self.hotkeys = []  # храним зарегистрированные горячие клавиши

    # --- Вспомогательные методы для работы со звуками ---

    def _play_sound(self, sound_name):
        """Проигрывает звук по имени (обращение к SoundManager)."""
        self.sound_manager.play(sound_name)

    def _on_shoot_callback(self, sound_name):
        """
            Коллбэк для выстрела: при выстреле вызывается этот метод
            который проигрывает звук выстрела или отсутствия патронов.
        """
        self._play_sound(sound_name)

    # --- Методы действий (обёртки с проверкой паузы) ---

    def _do_shoot(self):
        """Одиночный выстрел. Если управление отключено - ничего не делает."""
        if not self.control_enabled:
            return
        if self.turret.shoot():
            self._play_sound("shoot")
        else:
            self._play_sound("out_of_ammo")

    def _open_door(self):
        """Открыть дверь, если управление включено и дверь закрыта."""
        if self.control_enabled and self.door.open():
            self._play_sound("door_open")

    def _close_door(self):
        """Закрыть дверь, если управление включено и дверь открыта"""
        if self.control_enabled and self.door.close():
            self._play_sound("door_close")

    def _activate_turret(self):
        """Активировать турель, если управление включено и она ещё не активна"""
        if self.control_enabled and self.turret.activate():
            self._play_sound("turret_activate")

    def _deactivate_turret(self):
        """Деактивировать турель, если управление включено и она активна"""
        if self.control_enabled and self.turret.deactivate():
            self._play_sound("turret_deactivate")

    def _reload_turret(self):
        """Перезарядить турель до максимума (500), если управление включено"""
        if self.control_enabled and self.turret.reload():
            self._play_sound("reload")

    def _burst_fire_thread(self):
        """
            Запуск пулемётного режима в отдельном потоке.
            проверяет флаг, чтобы не запускать очередь в паузе.
        """
        if not self.control_enabled:
            return
        self.turret.burst_fire(self._on_shoot_callback)

    # --- Метод для устпновки произвольного количества патронов ---

    def _custom_reload(self):
        """
            Установка произвольного количества патронов (от 0 до 500).
            Вызывается по нажатию клавиши 'n'
            Временно отключает все горячие клавиши, чтобы ввод не перехватывался,
            запрашивает число, устанавливает боезапас, затем восстанавливает клавиши.
            Поддерживает знаки перед числом + и -.
            +N - добавить N патронов в пределах диапазона от 0 до 500
            -N - отнять N патронов но не ниже 0
            N  - установить абсолютное значение N (0-500)
        """
        if not self.control_enabled:
            return
        self.control_enabled = False
        print("\n[Турель] Введите количество патронов в пределах (0-500): 100, +50, -20)", end="", flush=True)
        # 2. Цикл ввода с проверкой корректности
        while True:
            raw = input().strip()
            if not raw:
                print("[Турель] Пустой ввод. Повторите: ", end="", flush=True)
                continue

            # Убираем всё, кроме цифр и знаков +-
            import re
            clean = re.sub(r'[^0-9+-]', '', raw)
            if not clean:
                print("[Турель] Ошибка: не найдены цифры. Повторите ввод: ", end="", flush=True)
                continue

            # Определяем знак
            sign = None             # Поумолчанию делаем пустой
            if '+' in clean and '-' not in clean:
                sign = '+'
                num_part = clean.replace('+', '')
            elif '-' in clean and '+' not in clean:
                sign = '-'
                num_part = clean.replace('-', '')
            elif '+' in clean and '-' in clean:
                if clean.find('+') < clean.find('-'):
                    sign = '+'
                    num_part = clean.replace('+', '')
                else:
                    sign = '-'
                    num_part = clean.replace('-', '')
            else:
                sign = None
                num_part = clean

            digits = re.sub(r'\D', '', num_part)
            if not digits:
                print("[Турель] Ошибка: не найдены цифры. Повторите ввод: ", end="", flush=True)
                continue

            number = int(digits)
            # Выполняем операцию
            current = self.turret.ammo
            max_ammo = self.turret.max_ammo

            if sign == '+':
                new_value = current + number
                if new_value > max_ammo:
                    added = max_ammo - current
                    new_ammo = new_value
                    print(f"[Турель] Добавлено только {added} патронов (магазин полон).")
                else:
                    print(f"[Турель] Добавлено {number} патронов.")
            elif sign == '-':
                new_value = current - number
                if new_value < 0:
                    removed = current
                    new_value = 0
                    print(f"[Турель] Снято {removed} патронов (больше нет).")
                else:
                    print(f"[Турель] Снято {number} патронов.")
            else:
                # Абсолютная установка
                if 0 <= number <= max_ammo:
                    new_value = number
                    print(f"[Турель] Боезапас установлен: {number}")
                else:
                    print(f"[Турель] Ошибка: число должно быть от 0 до {max_ammo}. Повторите ввод: ", end="", flush=True)
                    continue

            # Применяем новое значение (оно уже в диапазоне)
            self.turret.ammo = new_value
            print(f"[Турель] Текущий боезапас: {self.turret.ammo}")
            self._play_sound("reload")
            break

        self.control_enabled = True
        print("[Управление] Управление возобновлено.")

    # --- Управление паузой ---

    def _toggle_control(self):
        """Включает/выключает управление (режим паузы). Вызывается по нажатию alt+p."""
        self.control_enabled = not self.control_enabled
        status = "ВКЛЮЧЕНО" if self.control_enabled else "ВЫКЛЮЧЕНО (пауза)"
        print(f"\n[Управление] {status}. Нажмите alt+p для переключения.\n")

    def _register_hotkeys(self):
        """Регистрирует все горячие клавиши и сохраняет их идентификаторы в список self.hotkeys для последующего удаления."""
        self.hotkeys.append(keyboard.add_hotkey('o', self._open_door))
        self.hotkeys.append(keyboard.add_hotkey('c', self._close_door))
        self.hotkeys.append(keyboard.add_hotkey('a', self._activate_turret))
        self.hotkeys.append(keyboard.add_hotkey('d', self._deactivate_turret))
        self.hotkeys.append(keyboard.add_hotkey('r', self._reload_turret))
        self.hotkeys.append(keyboard.add_hotkey('n', self._custom_reload))
        self.hotkeys.append(keyboard.add_hotkey('f', self._do_shoot))
        self.hotkeys.append(keyboard.add_hotkey('b', lambda: threading.Thread(target=self._burst_fire_thread, daemon=True).start()))
        self.hotkeys.append(keyboard.add_hotkey('s', self.turret.stop))
        self.hotkeys.append(keyboard.add_hotkey('alt+p', self._toggle_control))

    # --- Главный цикл программы ---

    def run(self):
        """Запускает систему: выводит справку, регистрирует горячие клавиши и входит в цикл ожидания нажатия 'q' для выхода."""
        print("=== Автоматическая караульная система (со звуком) ===")
        self._show_help()
        print("Управление глобальное. Нажмите 'alt+p' для паузы.\n")

        self._register_hotkeys()

        # Цикл ожидания клавиши q (без блокировки, чтобы можно было выполнять input)
        while self.running:
            # Проверяем, не нажата ли q (можно использовать keyboard.is_pressed, но лучше событийно)
            # Для простоты оставим проверку в цикле
            if keyboard.is_pressed('q'):
                self.quit()
                break
            # Небольшая задержка для снижения нагрузки на процессор
            threading.Event().wait(0.1)

    # --- Выход из программы ---

    def quit(self):
        # Корректное завершение: отключает горячие клавиши, закрывает звук и завершает процесс.
        self.running = False
        print("Выход из системы охраны.")
        # Отключаем все горячие клавиши
        for h in self.hotkeys:
            keyboard.remove_hotkey(h)
        self.hotkeys.clear()
        self.sound_manager.quit()
        # Принудительно завершаем программу (чтобы не зависла)
        import sys
        sys.exit(0)

    # --- Справка ---

    def _show_help(self):
        """Выводит список доступных команд."""
        print("\n--- Управление караульной системой (клавиши) ---")
        print(" o - открыть дверь           ←/→     c - закрыть дверь")
        print(" a - активировать турель     ←/→     d - деактивировать турель")
        print(" r - перезарядить турель (до максимума)")
        print(" n - установить количество патронов (ввод числа)")
        print(" f - выстрелить один раз")
        print(" b - стрелять постоянно (пулемётный режим)")
        print(" s - остановить стрельбу")
        print(" q - выйти из системы")
        print(" alt+p - ВКЛ/ВЫКЛ управление (пауза)")
        print("-----------------------------\n")