import os
import sys
import io

# Автоматически переключаем кодировку консоли Windows на UTF-8 (только для Windows)
if sys.platform == "win32":
    try:
        os.system('chcp 65001 > nul')      # меняем консольную кодовую страницу
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass   # если что-то пошло не так, оставляем как есть

def generate_tree(startpath, prefix=""):
    """
    Рекурсивно обходит папки и возвращает список строк с деревом.
    """
    result = []
    # Получаем список папок и файлов, исключая скрытые директории (начинающиеся с точки)
    items = sorted(os.listdir(startpath))
    # Убираем системные папки, если надо (например, .git)
    items = [item for item in items if not item.startswith('.') and os.path.isdir(os.path.join(startpath, item))]
    items += [item for item in sorted(os.listdir(startpath)) if os.path.isfile(os.path.join(startpath, item))]
    # но проще: разделим на папки и файлы отдельно и отсортируем
    dirs = sorted([d for d in os.listdir(startpath) if os.path.isdir(os.path.join(startpath, d)) and not d.startswith('.')])
    files = sorted([f for f in os.listdir(startpath) if os.path.isfile(os.path.join(startpath, f))])

    # Собираем всё вместе: сначала папки, потом файлы
    entries = dirs + files
    count = len(entries)
    for i, entry in enumerate(entries):
        path = os.path.join(startpath, entry)
        is_last = (i == count - 1)
        # Выбираем символ для текущего уровня
        if is_last:
            connector = "└── "
        else:
            connector = "├── "

        result.append(prefix + connector + entry)

        # Если это папка, рекурсивно добавляем её содержимое
        if os.path.isdir(path):
            # Сдвигаем префикс для вложенных элементов
            if is_last:
                new_prefix = prefix + "    "  # 4 пробела
            else:
                new_prefix = prefix + "│   "
            result.extend(generate_tree(path, new_prefix))
    return result

def write_structure():
    # Решётка комментирует строку 
    # Переключаться можно между project_root = os.getcwd() и project_root = r"I:\" при помощи комментирования/раскомментирования
    project_root = os.getcwd()  # Текущая рабочая директория (папка проекта) # Закомментировать если нужно использовать назначение пути вручную
    # project_root = r"I:\" # Раскомментировать для использования и назначения пути вручную r"адрес\расположения"

    # Получаем название корневой папки
    root_name = os.path.basename(project_root)
    # Строим дерево, начиная с корневой папки
    lines = [root_name + "/"]
    # Для корневой папки передаём пустой префикс
    lines.extend(generate_tree(project_root, prefix=""))
    
    # Записываем в файл
    with open('Project_structure.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    # Печатаем сообщение в консоль (для корректного отображения русских символов в Windows)
    print('Структура проекта успешно создана в Project_structure.txt')

if __name__ == "__main__":
    write_structure()