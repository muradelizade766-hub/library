import unittest
from library import Library

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.library.books.clear()
        self.library.members.clear()

    def test_add_book(self):
        self.library.add_book("1", "Python", "John", "2026", "Programming")
        self.assertIn("1", self.library.books)
        self.assertEqual(self.library.books["1"].title, "Python")

    def test_remove_book(self):
        self.library.add_book("2", "Java", "Ali", "2024", "Robots")
        self.library.remove_book("2")
        self.assertNotIn("2", self.library.books)

    def test_search_books(self):
        self.library.add_book("3", "Python Programming", "Alice", "2025", "Code")
        results = self.library.search_books("Python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Python Programming")

    def test_register_member(self):
        self.library.register_member("1", "Bob")
        self.assertIn("1", self.library.members)
        self.assertEqual(self.library.members["1"].name, "Bob")

    def test_borrow_and_return_book(self):
        self.library.add_book("4", "Algorithms", "Charlie", "2023", "CS")
        self.library.register_member("2", "Diana")
        
        self.library.borrow_book("2", "4")
        self.assertTrue(self.library.books["4"].is_borrowed)

        self.library.return_book("2", "4")
        self.assertFalse(self.library.books["4"].is_borrowed)

if __name__ == "__main__":
    unittest.main()
