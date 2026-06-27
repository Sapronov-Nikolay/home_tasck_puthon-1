import pytest
from string_utils import StringUtils


string_utils = StringUtils()


@pytest.mark.positive
@pytest.mark.parametrize("input_str, expected", [
    ("skypro", "Skypro"),           # было SkyPro
    ("hello world", "Hello world"), # было Hello World
    ("python", "Python"),
])
def test_capitalize_positive(input_str, expected):
    assert string_utils.capitalize(input_str) == expected


@pytest.mark.negative
@pytest.mark.parametrize("input_str, expected", [
    ("123abc", "123abc"),
    ("", ""),
    ("   ", "   "),
])
def test_capitalize_negative(input_str, expected):
    assert string_utils.capitalize(input_str) == expected

# ===== Далее мои тесты =====
# ----- Тесты на trim переводится как "отделка, обшивка, подрезка"
"""
    Позитивные сценарии
    1. Строка с пробелами в начале → должны удалиться.
    2. Та же строка без пробелов в начале → должна остаться без изменений
    3. Строка в начале, внутри и в конце → должны удалиться только начальные
"""
@pytest.mark.positive
@pytest.mark.parametrize("input_str, expected", [
    ("   string", "string"),
    ("string", "string"),
    ("   string string  ", "string string  "),
])
def test_trim_positive(input_str, expected):
    assert string_utils.trim(input_str) == expected


"""
    Негативные сценарии
    1. Пустая строка → должна остаться пустой
    2. Строка из пробелов → должны быть удалены все пробелы
    3. Строка содержащая None → когда просто ничего нет
"""
@pytest.mark.negative
@pytest.mark.parametrize("input_str, expected", [
    ("", ""),
    ("   ", ""),
  # (None, "") # assert не умеет ловить исключения. Для проверки исключений нужно использовать pytest.raises.
])
def test_trim_negative(input_str, expected):
    assert string_utils.trim(input_str) == expected

# Негативный тест: передача None вместо строки. Используем pytest.raises
# Метод должен выбросить AttributeError, так как у None нет метода startswith().
# Мы говорим программе - не падай! None это не приговор, иди дальше
def test_trim_negative_none():
    with pytest.raises(AttributeError):
        string_utils.trim(None)


# ----- Тесты для contains Переводится как "содержать содержат"
"""
    Позитивные сценарии:
    1. Строка содержит искомый символ → True
    2. Строка не содержит искомый символ (символ не тот) → False
    3. Строка содержит часть текста (комбинацию букв) → True
    4. Строка содержит часть текста (не та часть) → False
    5. Строка с содержимым но когда мы не ищем ничего → True
    6. Строка просто пустая → True
    Мы не проверяем пробелы, так как тут проверяется содержание: оно есть или нет.
"""
@pytest.mark.positive
@pytest.mark.parametrize("string, symbol, expected", [
    ("SkyPro", "S", True),
    ("SkyPro", "U", False),
    ("SkyPro", "kyP", True),
    ("SkyPro", "rar", False),
    ("SkyPro", "", True),
    ("", "", True)
])
def test_contains_positive(string, symbol, expected):
    assert string_utils.contains(string, symbol) == expected
"""
    Негативные сценарии:
    1. В строку попало None, например из базы данных: Ошибка атрибута
    2. В строке есть текст, а случилось None, например из-за ошибки впрограмме: Ошибка типа данных
"""
@pytest.mark.negative
@pytest.mark.parametrize("string, symbol, expected", [
    (None, "SkayPro", AttributeError),
    ("SkayPro", None, TypeError)
])
def test_contains_negative_invalid_input(string, symbol, expected):
    with pytest.raises(expected):
        string_utils.contains(string, symbol)


# ----- Тест для delete_symbol переводится как "Удалить символ" -----
"""
    Позитивные сценарии:
    1. Найти и удалить символ
    2. Найти и удалить часть строки (комбинацию)
    3. Найти и удалить символ встречающийся не один раз
    4. Удаление не найденного символа → строка неизменна
"""
@pytest.mark.positive
@pytest.mark.parametrize("string, symbol, expected", [
    ("SkyPro", "S", "kyPro"),
    ("SkyPro", "Pro", "Sky"),
    ("abcabbaba", "b", "acaaa"),
    ("SkyPro", "F", "SkyPro")
])
def test_delete_symbol_positive(string, symbol, expected):
    assert string_utils.delete_symbol(string, symbol) == expected
"""
    Негативные сценарии (граничные случаи:
    1. Пустая строка и любой символ → остаётся пустая строка
    2. Текст есть а удаляем ничего → текст должен остаться без изменений = нечего удалять
    3. Передача None вместо строки → Оштбка AttributeError
    4. Передача строки вместо символа None → Ошибка TyprError
"""
@pytest.mark.negative
@pytest.mark.parametrize("string, symbol, expected", [
    ("", "a",""),      # Пустая строка должна остаться пустой
    ("ABC", "", "ABC")
])
def test_delete_symbol_negative_empty(string, symbol, expected):
    assert string_utils.delete_symbol(string, symbol) == expected

# Проверяем, что программа выбрасывает не что-то непонятное, а понятные ошибки
@pytest.mark.negative
@pytest.mark.parametrize("string, symbol, expected", [
    (None, "a", AttributeError),
    ("ABC", None, TypeError)
])
def test_delete_symbol_negative_none(string, symbol, expected):
    with pytest.raises(expected):
        string_utils.delete_symbol(string, symbol)