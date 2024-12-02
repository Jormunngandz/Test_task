import unittest
# from unittest import mock
# from unittest.mock import patch, Mock
from unittest.mock import patch, mock_open

import Library


class TestLibrary(unittest.TestCase):
    def setUp(self) -> None:
        # responses = {1}
        # fake_input = Mock(side_effect=1)
        # with patch(input, fake_input):
        self.library = Library.LibraryApp()

    def test_add_book(self):
        open_mock = mock_open()
        with patch("Library.open", open_mock, create=True):
            self.assertIsNone(self.library.add_book('Test book', 'Test author', '2005'))

    def test_delete_non_exists_book(self):
        open_mock = mock_open()
        with patch("Library.open", open_mock, create=True):
            self.assertIsNone(self.library.delete_book('20'))

    def test_delete_exists_book(self):
        expected_value = {'id': 4,
                          "title": "Test book",
                          "author": "Test author",
                          "published_data": "2005",
                          "status": "в наличии"}
        open_mock = mock_open()
        with patch("Library.open", open_mock, create=True):
            self.assertEqual(self.library.delete_book('4'), expected_value)

    def test_find_non_exists_book(self):
        self.assertEqual(self.library.find_book('non_exits_author', 'author'), [])

    def test_find_exists_book(self):
        expected_value = {'id': 4,
                          "title": "Test book",
                          "author": "Test author",
                          "published_data": "2005",
                          "status": "в наличии"}
        self.assertIn(expected_value, self.library.find_book('Test book', 'title'))

    def test_set_incorrect_status(self):
        open_mock = mock_open()
        with patch("Library.open", open_mock, create=True):
            self.assertIsNone(self.library.change_book_status(3, 'wrong_case'))

    def test_set_correct_status(self):
        open_mock = mock_open()
        with patch("Library.open", open_mock, create=True):
            self.assertEqual(self.library.change_book_status(3, '1'), 3)

    def test_set_status_with_non_exists_index(self):
        open_mock = mock_open()
        with patch("Library.open", open_mock, create=True):
            self.assertIsNone(self.library.change_book_status(33, '1'))


if __name__ == '__main__':
    unittest.main()
