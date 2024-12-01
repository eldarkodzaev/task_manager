# Python 3.12.5
#
# Консольное приложение "Менеджер задач".
#
# Приложение для управления списком задач с возможностью добавления,
# выполнения, удаления и поиска задач.


import colorama

from managers import TaskManager
from menu import menu, print_menu


def main(manager: TaskManager):
    while True:
        print_menu()
        action = input(">>> ")
        if action == "0":
            print("Программа завершена")
            break
        if action not in menu:
            print(colorama.Fore.RED + "Неверный ввод. Повторите еще раз.")
        else:
            menu[action](manager)


if __name__ == "__main__":
    colorama.init(autoreset=True)
    
    file = input("Введите имя файла базы данных: ")
    manager = TaskManager(file)
    
    main(manager)
