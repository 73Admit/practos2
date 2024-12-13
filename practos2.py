class BookStore:
    def __init__(self):
        self.users = []
        self.books = [{'title': 'Война и мир', 'author': 'Лев Толстой', 'price': 500},
            {'title': '1984', 'author': 'Джордж Оруэлл', 'price': 300},
            {'title': 'Мастер и Маргарита', 'author': 'Михаил Булгаков', 'price': 400},
            {'title': 'Преступление и наказание', 'author': 'Фёдор Достоевский', 'price': 350},
            {'title': 'Анна Каренина', 'author': 'Лев Толстой', 'price': 450},
            ]
        self.current_user = None

    def add_user(self, username, password, role='user'):
        user = {
            'username': username,
            'password': password,
            'role': role,
            'purchase_history': []
        }
        self.users.append(user)

    def add_book(self, title, author, price):
        try:
            price = float(price)
            if price <= 0:
                raise ValueError("\nЦена должна быть положительным числом.")
            if not title or not author:
                raise ValueError("\nНазвание и автор книги не могут быть пустыми.")
            self.books.append({'title': title, 'author': author, 'price': price})
            print("\n------\n")
            print(f"\nКнига '{title}' добавлена.\n")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def login(self, username, password):
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                return True
        return False

    def view_books(self):
        if self.books:
            print("\nДоступные книги:\n------")
            for book in self.books:
                print(f"- {book['title']} от {book['author']}, цена: {book['price']} руб.")
            print("------\n")    
        else:
            print("Нет доступных книг.")

    def buy_book(self, title):
        if not self.current_user:
            print("\nПожалуйста, войдите в систему.")
            return

        for book in self.books:
            if book['title'] == title:
                self.current_user['purchase_history'].append(book)
                print(f"\nВы купили книгу: {book['title']}")
                return
        print("Книга не найдена.")

    def search_book(self, title):
        results = list(filter(lambda book: title.lower() in book['title'].lower(), self.books))
        if results:
            print("\nРезультаты поиска книг:")
            for book in results:
                print(f"- {book['title']} от {book['author']}, цена: {book['price']} руб.")
        else:
            print("Книги не найдены.")

    def filter_and_sort_books(self, filters=None, sort_by=None):
        filtered_books = list(self.books)

        if filters:
            for key, value in filters.items():
                filtered_books = list(filter(lambda book: book[key] <= value, filtered_books))

        if sort_by:
            filtered_books = sorted(filtered_books, key=lambda book: tuple(book[criteria] for criteria in sort_by))

        if filtered_books:
            print("\nОтфильтрованные и отсортированные книги:")
            for book in filtered_books:
                print(f"- {book['title']} от {book['author']}, цена: {book['price']} руб.\n------\n")
        else:
            print("\nКниги не соответствуют критериям фильтрации.")

    def view_purchase_history(self):
        if not self.current_user:
            print("\nПожалуйста, войдите в систему.")
            return

        if self.current_user['purchase_history']:
            print("\nВаша история покупок:")
            for book in self.current_user['purchase_history']:
                print(f"- {book['title']}")
        else:
            print("Вы еще ничего не купили.")

    def filter_books(self, criterion, threshold):
        filtered_books = list(filter(lambda book: book[criterion] <= threshold, self.books))
        if filtered_books:
            print("Отфильтрованные книги:")
            for book in filtered_books:
                print(f"- {book['title']} от {book['author']}, цена: {book['price']} руб.")
        else:
            print("Книги не соответствуют критериям фильтрации.")

    def search_user(self, username):
        results = list(filter(lambda user: username.lower() in user['username'].lower(), self.users))
        if results:
            print("\nРезультаты поиска пользователей:\n-------\n")
            for user in results:
                print(f"- {user['username']} ({user['role']})\n")
        else:
            print("\nПользователи не найдены.")

    def user_menu(self):
        while True:
            print("\nПользовательское меню:\n------")
            print("1. Просмотреть книги")
            print("2. Купить книгу")
            print("3. Посмотреть историю покупок")
            print("4. Фильтрация и сортировка книг")
            print("5. Поиск книги по названию")
            print("0. Выйти\n------\n")
            choice = input("Выберите действие: ")

            if choice == '1':
                self.view_books()
            elif choice == '2':
                title = input("\n------\nВведите название книги для покупки: ")
                self.buy_book(title)
            elif choice == '3':
                self.view_purchase_history()
            elif choice == '4':
                filters = {}
                if input("\n-----\nФильтровать по цене? (y/n): ").lower() == 'y':
                    max_price = float(input("\nВведите максимальную цену для фильтрации: "))
                    filters['price'] = max_price
                    
                
                sort_by = input("\nВведите параметры сортировки через запятую (title, author, price) или нажмите Enter для пропуска: ")
                sort_by = sort_by.split(',') if sort_by else None
                self.filter_and_sort_books(filters, sort_by)
            elif choice == '5':
                title = input("\nВведите название книги для поиска: ")
                self.search_book(title)
            elif choice == '0':
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    def admin_menu(self):
        if not self.current_user or self.current_user['role'] != 'admin':
            print("У вас нет доступа к администраторскому меню.")
            return

        while True:
            print("\nАдминистраторское меню:\n------")
            print("1. Добавить книгу")
            print("2. Удалить книгу")
            print("3. Редактировать книгу")
            print("4. Просмотреть список пользователей")
            print("5. Поиск пользователя")
            print("0. Выйти\n-------")
            try:
                choice = input("Выберите действие: ")
                if choice == '1':
                    title = input("\nВведите название книги: ")
                    author = input("Введите автора книги: ")
                    while True:
                        try:
                            price = float(input("Введите цену книги: "))
                            if price <=0:
                                raise ValueError("\nЦена должна быть положительным числом.")
                            break
                        except ValueError as e:
                            print(f"Ошибка: {e}")
                    self.add_book(title, author, price)
                elif choice == '2':
                    title = input("\nВведите название книги для удаления: ")
                    if any(book['title'] == title for book in self.books):
                        self.books = [book for book in self.books if book['title'] != title]
                        print(f"\nКнига '{title}' удалена.")
                    else:
                        print(f"\nКнига '{title}' не найдена.")

                elif choice == '3':
                    title = input("\n-----\nВведите название книги для редактирования: ")
                    book_found = False
                    for book in self.books:
                        if book['title'] == title:
                            while True:
                                try:
                                    new_price = float(input("Введите новую цену книги: "))
                                    if new_price <= 0:
                                        raise ValueError("\nЦена должна быть положительным числом.")
                                    break
                                except ValueError as e:
                                    print(f"\nОшибка: {e}")
                            book['title'] = input("Введите новое название книги: ") or book['title']
                            book['author'] = input("Введите нового автора книги: ") or book['author']
                            book['price'] = new_price
                            print("\n------\n")
                            print(f"\nКнига '{title}' обновлена.\n")
                            book_found = True
                            break
                    if not book_found:
                        print("Книга не найдена.")
                elif choice == '4':
                    print("\n-------\nСписок пользователей:")
                    for user in self.users:
                        print(f"- {user['username']} ({user['role']})")
                elif choice == '5':
                    username = input("\n------\nВведите логин пользователя для поиска: ")
                    self.search_user(username)
                elif choice == '0':
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")
            except ValueError as e:
                print(f"Ошибка: {e}")
            except Exception as e:
                print(f"Произошла непредвиденная ошибка: {e}")
                
    def register_user(self):
        username = input("\nВведите логин для нового пользователя: ")
        password = input("Введите пароль для нового пользователя: ")
        self.add_user(username, password)
        print(f"\nПользователь {username} успешно зарегистрирован!")

    def run(self):
        while True:
            print("\n-------\n1. Войти в систему")
            print("2. Зарегистрироваться")
            print("0. Выйти\n-------")
            choice = input("\nВыберите действие: ")

            if choice == '1':
                username = input("\n-----\nЛогин: ")
                password = input("Пароль: ")
                print("-----")
                if self.login(username, password):
                    print(f"Добро пожаловать, {self.current_user['username']}!")
                    if self.current_user['role'] == 'admin':
                        self.admin_menu()
                    else:
                        self.user_menu()
                else:
                    print("\nНеправильный логин или пароль.")
            elif choice == '2':
                self.register_user()
            elif choice == '0':
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    store = BookStore()
    store.add_user('admin', 'admin123', role='admin')
    store.add_user('danil', 'password')
    print("\nДобро пожаловать в книжный магазин!")
    store.run()