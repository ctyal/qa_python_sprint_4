from main import BooksCollector
import pytest


class TestBooksCollector:
    
    # Добавление книг
    # тесты на добавление книги
    def test_add_new_book_add_one_book(self, collector):
        collector.add_new_book('Наваждения')
        assert 'Наваждения' in collector.get_books_genre(), 'Failed. Книга не добавилась'

    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2, 'Failed. Книги не добавились'

    def test_add_new_book_one_book_twice_one_book_added(self, collector):
        collector.add_new_book('Незнакомец')
        collector.add_new_book('Незнакомец')
        assert len(collector.get_books_genre()) == 1, 'Failed. Добавляется дубль книги'

    # тесты добавления книги: валидное число символов в названии (1, 2, 39, 40)
    @pytest.mark.parametrize('book', ['А', 'А'*2, 'А'*39, 'А'*40])
    def test_add_new_book_valid_name_lenght_added(self, collector, book):
        collector.add_new_book(book)
        assert book in collector.get_books_genre(), f"Failed. Книга с названием допустимой длины в {len(book)} симв не добавилась."
    
    # тесты добавления книги: невалидное число символов в названии (0, 41, 45)
    @pytest.mark.parametrize('invalid_name', ['', 'А'*41, 'А'*45])
    def test_add_new_book_invalid_name_lenght_not_added(self, collector, invalid_name):
        collector.add_new_book(invalid_name)
        assert invalid_name not in collector.get_books_genre(), f"Failed. Книга с названием недопустимой длины в {len(invalid_name)} симв добавилась."

    # Жанр
    # тесты добавления жанра
    def test_add_new_book_has_no_genre_by_default_true(self, collector):
        collector.add_new_book('Незнакомец')
        assert collector.get_book_genre('Незнакомец') == '', 'Failed. Жанр книги не пустой по умолчанию'

    def test_set_book_genre_existing_genre_added(self, collector):
        collector.add_new_book('Незнакомец')
        collector.set_book_genre('Незнакомец', 'Комедии')
        assert collector.get_book_genre('Незнакомец') == 'Комедии', 'Failed. Книге не добавился жанр из списка допустимых жанров'

    def test_set_book_genre_nonexistent_genre_not_added(self, collector):
        collector.add_new_book('Незнакомец')
        collector.set_book_genre('Незнакомец', 'Мистика')
        assert collector.get_book_genre('Незнакомец') == '', 'Failed. Книге добавился жанр, которого нет в списке допустимых жанров'

    def test_set_book_genre_existing_genre_to_nonexistent_book_not_added(self, collector):
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дина', 'Ужасы')
        assert collector.get_books_genre().get('Дина') is None, 'Failed. Несуществующей книге добавился жанр'

    # тесты вывода по жанру
    def test_set_book_genre_existenting_genre_two_books_added_returns_dict(self, collector):
        collector.books_genre = {'Шутка': 'Комедии', 'Шутка Два': 'Комедии', 'Оно': 'Ужасы'}
        comedy = collector.get_books_with_specific_genre('Комедии')
        assert len(comedy) == 2 and 'Шутка' in comedy and 'Шутка Два' in comedy

    def test_get_books_genre_returns_current_dict(self, collector):
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Ужасы')
        collector.add_new_book('Незнакомец')
        collector.set_book_genre('Незнакомец', 'Комедии')
        genre_dict = collector.get_books_genre()
        assert genre_dict == {'Дюна': 'Ужасы', 'Незнакомец': 'Комедии'}

    def test_get_books_genre_empty_dict_by_default(self, collector):
        genre_dict = collector.get_books_genre()
        assert genre_dict == {}

    # тесты книг для детей
    def test_get_books_for_children_excludes_age_rating_books(self, collector):
        collector.add_new_book('Смешарики')
        collector.set_book_genre('Смешарики', 'Мультфильмы')
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')

        books_for_children = collector.get_books_for_children()
        assert 'Оно' not in books_for_children, 'В детские книги добавилась книга жанра, которого нет в списке допустимых для детей жанров'

    # Избранное
    # тесты добавления в избраное
    def test_add_book_in_favorites_add_existing_book_added(self, collector):
        collector.add_new_book('Смешарики')
        collector.add_book_in_favorites('Смешарики')
        fav_list = collector.get_list_of_favorites_books()
        assert 'Смешарики' in fav_list, 'Failed. В избранное не добавилась книга'

    def test_add_book_in_favorites_add_existing_book_twice_added_one_entry(self, collector):
        collector.add_new_book('Смешарики')
        collector.add_book_in_favorites('Смешарики')
        collector.add_book_in_favorites('Смешарики')
        fav_list = collector.get_list_of_favorites_books()
        assert len(fav_list) == 1, 'Failed. В избранное добавляется дубль книги'

    def test_add_book_in_favorites_add_nonexistent_book_not_added(self, collector):
        collector.add_book_in_favorites('Смешарики')
        fav_list = collector.get_list_of_favorites_books()
        assert len(fav_list) == 0, 'Failed. В избранное добавляется несуществующая книга'   

    # тесты удаления из избранного
    def test_delete_book_from_favorites_existing_book_deleted(self, collector):
        collector.add_new_book('Смешарики')
        collector.add_book_in_favorites('Смешарики')
        collector.delete_book_from_favorites('Смешарики')
        fav_list = collector.get_list_of_favorites_books()
        assert len(fav_list) == 0, 'Failed. Из избранного не удаляется книга'

    def test_delete_book_from_favorites_nonexistent_book_not_deleted(self, collector):
        collector.add_new_book('Смешарики')
        collector.add_book_in_favorites('Смешарики')
        collector.delete_book_from_favorites('Незнакомец')
        fav_list = collector.get_list_of_favorites_books()
        assert len(fav_list) == 1 and 'Смешарики' in fav_list, 'Failed. Список избранного изменился при попытке удалить несуществующую книгу'
