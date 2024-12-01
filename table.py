from prettytable import PrettyTable


field_names = [
    'ID', 'Статус', 'Заголовок', 'Описание', 'Категория', 'Срок выполнения', 'Приоритет'
]

def fill_table(data: list) -> None:
    table = PrettyTable()
    table.field_names = field_names
    table.add_rows(data)
    return table
