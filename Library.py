import datetime
import json
from os import system, name
from typing import List, Dict, Union, Tuple, Any


def clear() -> None:
    """Функция для очистки консоли, работает с UNIX, Windows системами """
    # for windows
    if name == 'nt':
        system('cls')
    # for mac and linux
    else:
        system('clear')


class LibraryApp:
    def __init__(self):
        """При инициализации создается либо читается json-файл с данными об имеющихся книгах."""
        try:
            with open('Data.json', 'r') as datafile:
                self.database = json.load(datafile)
        except FileNotFoundError:
            self.database: List[Dict] = []
            with open('Data.json', 'w') as datafile:
                json.dump(self.database, datafile)

        # self.process()

    def process(self) -> None:
        """Метод обеспечивающая работу главного меню приложения"""
        print('Вас приветствует электронная система управление библиотекой!')
        print('Для того чтобы выбрать пункт меню введите его номер (например: "1")')
        while True:
            self.print_interface()
            if not self.database:
                print("\nВ библиотеке пока нет книг\n")
            user_input: str = input("Ввод: ")

            match user_input:
                case '1':
                    self.add_book_inputs()
                case '2':
                    self.delete_book_inputs()
                case '3':
                    self.find_book_inputs()
                case '4':
                    self.show_books()
                    input("Нажмите Enter чтобы продолжить")
                case '5':
                    self.change_book_status_input()
                case 'exit':
                    return
                case _:
                    input("Некорректный ввод. Нажмите Enter")
            clear()

    def add_book_inputs(self) -> None:
        """Метод принимает и валидирует пользовательские вводы, если данные корректны, то
        вызывается функция добавления книги add_book"""
        while True:
            clear()
            while True:
                title: str = input('Введите название книги (оставьте пустым чтобы выйти): ')
                if len(title) > 0:
                    clear()
                    break
                return
            while True:
                author: str = input('Введите имя автора книги (оставьте пустым чтобы выйти): ')
                if len(author) > 0:
                    clear()
                    break
                return
            while True:
                year: str = input('Введите год публикации книги (оставьте пустым чтобы выйти): ')
                if year.isdigit() and int(datetime.datetime.today().year) >= int(year) > 0:
                    break
                elif not year:
                    return
                input('Некорректная дата! Нажмите Enter чтобы продолжить.')
                clear()
            self.add_book(title, author, year)
            user_input: str = input("Книга успешно добавлена. Вернуться в меню? (y/n)")
            if user_input.lower() == 'y':
                return

    def add_book(self, title: str, author: str, year: str) -> None:
        """Метод пронимает валидированные данные и добавляет книгу к списку имеющихся, а так же записывает обновленные
        данные в json-файл"""
        self.database.append({'id': self.database[-1]['id'] + 1 if self.database else 1,
                              'title': title,
                              'author': author,
                              "published_data": year,
                              'status': "в наличии"
                              })
        with open('Data.json', 'w') as datafile:
            json.dump(self.database, datafile)

    def delete_book_inputs(self) -> None:
        """Метод принимает и валидирует пользовательские вводы, если данные корректны, то
        вызывается функция удаления книги delete_book"""
        clear()
        while True:
            book_id: str = input('Введите id книги которую нужно удалить: ')
            if book_id and book_id.isdigit():
                break
            print("Некорректный ID")
            print()
        deleted_book: Union[None, Dict] = self.delete_book(book_id)
        if deleted_book:
            input(f'Книга {deleted_book["title"]} успешно удалена. Нажмите Enter чтобы продолжить.')
        else:
            input(f"Книги под номером {book_id} не существует в библиотеке. Нажмите Enter чтобы продолжить.")

    def delete_book(self, book_id: str) -> Union[None, Dict]:
        """Метод ищет книгу с заданным id и удаляет ее из списка, а так же обновляет json-файл"""
        result: Union[None, Tuple] = self.find_book_by_id(int(book_id))
        if not result:
            return
        index, value = result
        del self.database[index]
        with open('Data.json', 'w') as datafile:
            json.dump(self.database, datafile)
        return value

    def find_book_inputs(self):
        """Метод принимает и валидирует пользовательские вводы, если данные корректны, то
        вызывается функция поиска книги find_book"""
        clear()
        print("Поиск по: \n\t1.Названию\n\t2.Имени автора\n\t3.Году публикации")
        print('Enter чтобы вернуться в меню')
        user_input: str = input("Ввод: ")
        match user_input:
            case '1':
                key: str = 'title'
                find_value: str = input('Введите название книги: ')
            case '2':
                key: str = 'author'
                find_value: str = input('Введите имя автора: ')
            case '3':
                key: str = 'published_data'
                find_value: str = input('Введите дату публикации: ')
                if not find_value.isdigit() or not int(datetime.datetime.today().year) >= int(find_value) > 0:
                    input('Некорректный ввод. Нажмите Enter.')
                    return
            case _:
                input('Некорректный ввод. Нажмите Enter.')
                return
        result: List[Dict] = self.find_book(find_value, key)

        if result:
            self.show_books(result)
            input("Нажмите Enter чтобы продолжить.")
        else:
            input("Результат поиска отсутствует. Нажмите Enter чтобы продолжить.")

    def find_book(self, find_value: str, key: str) -> Union[None, List[Dict]]:
        """Метод ищет и возвращает список книг, которые удовлетворяют переданным критериям поиска"""
        return list(filter(lambda x: x[key] in find_value or find_value in x[key], self.database))

    def find_book_by_id(self, id_value: int) -> Union[None, Tuple[int, Dict]]:
        """Метод ищет книгу с заданным id и возвращает его номер в списке книг, если книга с таким id существует"""
        for i, book_data in enumerate(self.database):
            if book_data['id'] == id_value:
                return i, book_data

    def show_books(self, books: Union[None, List[Dict]] = None) -> None:
        """Метод отображает передаваемый список книг в табличном формате, если список не передан, то отображает
         все книги, которые имеются в списке книг библиотеки"""
        clear()
        if not books:
            books = self.database
            """Определяем самое длинное название книги, а так же длинну имени автора"""
        try:
            max_length_title: int = max(len(max(books, key=lambda x: len(x['title']))['title']), 15)
            max_length_author: int = max(len(max(books, key=lambda x: len(x['author']))['author']), 15)
        except ValueError:
            max_length_title = 15
            max_length_author = 15
        print("{:<8} {:<{title}} {:<{author}} {:<14} {:<14}".format(
            'ID',
            'Название',
            'Автор',
            'Год публикации',
            'Статус',
            title=max_length_title,
            author=max_length_author))

        for book in books:
            print("{:<8} {:<{title}} {:<{author}} {:<14} {:<14}".format(book['id'],
                                                                        book['title'],
                                                                        book['author'],
                                                                        book['published_data'],
                                                                        book['status'],
                                                                        title=max_length_title,
                                                                        author=max_length_author))

    def change_book_status_input(self) -> None:
        """Метод принимает и валидирует пользовательские вводы, если данные корректны, то
        вызывается функция обновления статуса книги change_book_status"""
        clear()
        while True:
            book_id: str = input('Введите id книги статус которой нужно сменить: ')
            if book_id and book_id.isdigit():
                break
            print("Некорректный ID")
            print()
        result: Union[None, Tuple] = self.find_book_by_id(int(book_id))
        if not result:
            input('Книга не найдена. Нажмите Enter.')
            return
        index, value = result
        print(f'Изменить статус книги: \t\n1.В наличии {"(текущий статус)" if value["status"] == "в наличии" else ""}'
              f'\t\n2.Выдана {"(текущий статус)" if value["status"] == "выдана" else ""}')
        user_input: str = input("Ввод: ")
        result = self.change_book_status(index, user_input)
        if result:
            input(f"Статус книги {result} успешно изменен. Нажмите Enter.")
        else:
            input('Неверный ввод. Нажмите Enter.')

    def change_book_status(self, index: int, user_option: str) -> Any:
        """Метод изменяет статус книги с соответсвующим индексом"""
        try:
            match user_option:
                case '1':
                    self.database[index]['status'] = "в наличии"
                case '2':
                    self.database[index]['status'] = "выдана"
                case _:
                    return
            with open('Data.json', 'w') as datafile:
                json.dump(self.database, datafile)
            return index
        except IndexError:
            return

    @staticmethod
    def print_interface() -> None:
        """Метод отвечает за отображение интерфейса главного меню"""
        print("1.Добавить книгу \n2.Удалить книгу \n3.Найти книгу \n4.Список книг \n5.Взять/Сдать книгу")


if __name__ == '__main__':
    LibraryApp().process()
