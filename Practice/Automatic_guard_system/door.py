# Класс Door управляет дверью: открывает и закрывает.
# Звуки не встроены в класс, чтобы дверь была независимой.
# Звуки будут проигрываться из SecuritySystem.

class Door:
    def __init__(self):
        # is_open = False → дверь закрыта, True → открыта
        self.is_open = False

    def open(self):
        """
            Открыть дверь, если она закрыта.
            Возвращает True, если дверь была закрыта и мы её открыли,
            иначе False (если уже открыта)
        """
        if not self.is_open:
            self.is_open = True
            print("[Дверь] Открыта")
            return True
        else:
            print("[Дверь] Уже открыта")
            return False

    def close(self):
        """
            Закрыть дверь, если она открыта.
            Возвращает True, если дверь была открыта и мы её закрыли,
            иначе False (если уже закрыта)
        """
        if self.is_open:
            self.is_open = False
            print("[Дверь] Закрыта")
            return True
        else:
            print("[Дверь] Уже закрыта")
            return False