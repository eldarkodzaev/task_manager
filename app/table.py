# Модуль для работы с таблицей PrettyTable.
# Это таблица, которая выводится в консоль при выборе пользователем, например,
# опции "Посмотреть все задачи"


from prettytable import PrettyTable


field_names = [
    'ID', 'Статус', 'Заголовок', 'Описание', 'Категория', 'Срок выполнения', 'Приоритет'
]

def fill_table(data: list) -> None:
    """Заполняет таблицу PrettyTable данными.

    Параметры:
        data (list): список с данными
    """
    table = PrettyTable()
    table.field_names = field_names
    table.add_rows(data)
    return table
