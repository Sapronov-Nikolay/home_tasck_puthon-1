# Класс SoundManager загружает и воспроизводит звуки (WAV).
# Инициализирует pygame.mixer. Загружает звуки из папки media/ и хранит их в словаре.

import pygame, os

class SoundManager:
    # Инициализация звуковой системы pygame
    def __init__(self, media_folder="media"):
        pygame.mixer.init()     # Запускаем звуковую систему
        self.media_folder = media_folder    # папка со звуками
        self.sounds = {}        # словарь {имя_ключа: pygame.Sound}

    def load_sound(self, name, filename):
        """
        Загружает звуковой файл из папки media.
        name - ключ, по которому будем воспроизводить (например, "shoot")
        filename - имя файла (например, "shoot.wav")
        """
        path = os.path.join(self.media_folder, filename)
        if os.path.exists(path):
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
                print(f"Звук {name} загружен из {path}")
            except Exception as e:
                print(f"Ошибка загрузки {name}: {e}")
        else:
            print(f"Предупреждение: файл {path} не найден, звук {name} не будет воспроизводиться")

    def play(self, name):
        """Воспроизводит звук по ключу, если он загружен"""
        if name in self.sounds:
            self.sounds[name].play()
            # Для отладки можно раскомментировать следующую строку:
            # print(f"Воспроизведение звука: {name}")    # Временная проверка
        else:
            print(f"Звук {name} не найден!")

    def quit(self):
        """Завершает работу звуковой системы (вызывается при выходе)."""
        pygame.quit()