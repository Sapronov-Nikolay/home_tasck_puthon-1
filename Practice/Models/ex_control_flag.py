# ex_control_flag.py
# Цель: показать, как флаг control_enabled блокирует выполнение команд.
import time, keyboard

control_enabled = True

def do_action(name):
    if control_enabled:
        print(f"Выполняю: {name}")
    else:
        print(f"Игнорирую: {name} (управление отключено")

def toggle():
    global control_enabled
    control_enabled = not control_enabled
    print(f"Управление {'включено' if control_enabled else 'выключено'}")

keyboard.add_hotkey('a', lambda: do_action('A'))
keyboard.add_hotkey('b', lambda: do_action('B'))
keyboard.add_hotkey('p', toggle)
keyboard.add_hotkey('q', lambda: exit(0))

print("Нажмите a или b - выполнится действие. p - переключить флаг. q - выход")
keyboard.wait('q')