from models import Book, Member
from file_manager import FileManager
from validators import Validator


class Library:
    """Class to manage library operations, books, and members."""

    def __init__(self, books_file="data/books.txt", members_file="data/members.txt"):
        self.books_file = books_file
        self.members_file = members_file
        self.books = {}
        self.members = {}
        self.load_data()

    def load_data(self):
        """Loads books and members from text files into memory."""
        self.books.clear()
        self.members.clear()

        book_lines = FileManager.load_from_text(self.books_file)
        for line in book_lines:
            parts = line.split("|")
            if len(parts) == 4:
                book_id, title, author, is_borrowed = parts
                self.books[book_id] = Book(
                    book_id=book_id,
                    title=title,
                    author=author,
                    is_borrowed=(is_borrowed.lower() == "true")
                )

        member_lines = FileManager.load_from_text(self.members_file)
        for line in member_lines:
            parts = line.split("|")
            if len(parts) >= 2:
                member_id = parts[0]
                name = parts[1]
                borrowed_books = parts[2].split(",") if len(parts) > 2 and parts[2] else []
                self.members[member_id] = Member(
                    member_id=member_id,
                    name=name,
                    borrowed_books=borrowed_books
                )

    def save_data(self):
        """Saves current memory state of books and members back to text files."""
        book_lines = [
            f"{book.book_id}|{book.title}|{book.author}|{book.is_borrowed}"
            for book in self.books.values()
        ]
        FileManager.save_to_text(self.books_file, book_lines)

        member_lines = [
            f"{member.member_id}|{member.name}|{','.join(member.borrowed_books)}"
            for member in self.members.values()
        ]
        FileManager.save_to_text(self.members_file, member_lines)

    def add_book(self, book_id, title, author):
        """Adds a new book to the library."""
        book_id = Validator.validate_id(book_id, "Book ID")
        title = Validator.validate_not_empty(title, "Title")
        author = Validator.validate_not_empty(author, "Author")

        if book_id in self.books:
            raise ValueError(f"Book with ID '{book_id}' already exists!")

        new_book = Book(book_id, title, author)
        self.books[book_id] = new_book
        self.save_data()
        return new_book

    def remove_book(self, book_id):
        """Removes a book from the library by ID."""
        book_id = Validator.validate_id(book_id, "Book ID")
        if book_id not in self.books:
            raise ValueError(f"Book with ID '{book_id}' not found!")

        if self.books[book_id].is_borrowed:
            raise ValueError("Cannot remove a book that is currently borrowed!")

        del self.books[book_id]
        self.save_data()

    def register_member(self, member_id, name):
        """Registers a new member to the library."""
        member_id = Validator.validate_id(member_id, "Member ID")
        name = Validator.validate_not_empty(name, "Member Name")

        if member_id in self.members:
            raise ValueError(f"Member with ID '{member_id}' already exists!")

        new_member = Member(member_id, name)
        self.members[member_id] = new_member
        self.save_data()
        return new_member

    def borrow_book(self, member_id, book_id):
        """Borrows a book for a member."""
        member_id = Validator.validate_id(member_id, "Member ID")
        book_id = Validator.validate_id(book_id, "Book ID")

        if member_id not in self.members:
            raise ValueError(f"Member with ID '{member_id}' not found!")
        if book_id not in self.books:
            raise ValueError(f"Book with ID '{book_id}' not found!")

        book = self.books[book_id]
        member = self.members[member_id]

        if book.is_borrowed:
            raise ValueError(f"Book '{book.title}' is already borrowed!")

        book.is_borrowed = True
        member.borrow_book(book_id)
        self.save_data()

    def return_book(self, member_id, book_id):
        """Returns a borrowed book back to the library."""
        member_id = Validator.validate_id(member_id, "Member ID")
        book_id = Validator.validate_id(book_id, "Book ID")

        if member_id not in self.members:
            raise ValueError(f"Member with ID '{member_id}' not found!")
        if book_id not in self.books:
            raise ValueError(f"Book with ID '{book_id}' not found!")

        book = self.books[book_id]
        member = self.members[member_id]

        if book_id not in member.borrowed_books:
            raise ValueError(f"Member '{member.name}' has not borrowed this book!")

        book.is_borrowed = False
        member.return_book(book_id)
        self.save_data()

    def search_books(self, query):
        """Searches books by title or author."""
        query = query.lower().strip()
        return [
            book for book in self.books.values()
            if query in book.title.lower() or query in book.author.lower()
        ]
