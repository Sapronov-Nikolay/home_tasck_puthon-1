# Точка входа в программу. Инициализирует звуки, создаёт систему и запускает.

from sound_manager import SoundManager
from security_system import SecuritySystem

def main():
    # Создаём менеджер звуков, указываем папку с аудиофайлами
    sound_mqr = SoundManager("media")

    # Загружаем звуки (имена файлов должны точно соответствовать тем, что лежат в media)
    sound_mqr.load_sound("door_open", "door_open.wav")
    sound_mqr.load_sound("door_close", "door_close.wav")
    sound_mqr.load_sound("turret_activate", "turret_activate.wav")
    sound_mqr.load_sound("turret_deactivate", "turret_deactivate.wav")
    sound_mqr.load_sound("reload", "reload.wav")
    sound_mqr.load_sound("shoot", "shoot.wav")
    sound_mqr.load_sound("out_of_ammo", "out_of_ammo.wav")

    # Создаём систему безопасности и передаём ей звуковой менеджер
    system = SecuritySystem(sound_mqr)

    # Запускаем
    system.run()

if __name__ == "__main__":
    main()