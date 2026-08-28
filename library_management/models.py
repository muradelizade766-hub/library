class Book:
    """Class representing a book entity."""
    
    def __init__(self, book_id, title, author, is_borrowed=False):
        self._book_id = book_id
        self._title = title
        self._author = author
        self._is_borrowed = is_borrowed

    @property
    def book_id(self):
        return self._book_id

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def is_borrowed(self):
        return self._is_borrowed

    @is_borrowed.setter
    def is_borrowed(self, status):
        self._is_borrowed = status

    def to_dict(self):
        """Converts the Book object to a dictionary."""
        return {
            "book_id": self._book_id,
            "title": self._title,
            "author": self._author,
            "is_borrowed": self._is_borrowed
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Book object from a dictionary."""
        return cls(
            book_id=data["book_id"],
            title=data["title"],
            author=data["author"],
            is_borrowed=data.get("is_borrowed", False)
        )

    def __str__(self):
        status = "Borrowed" if self._is_borrowed else "Available"
        return f"[{self._book_id}] {self._title} by {self._author} ({status})"


class Member:
    """Class representing a library member entity."""
    
    def __init__(self, member_id, name, borrowed_books=None):
        self._member_id = member_id
        self._name = name
        self._borrowed_books = borrowed_books if borrowed_books is not None else []

    @property
    def member_id(self):
        return self._member_id

    @property
    def name(self):
        return self._name

    @property
    def borrowed_books(self):
        return self._borrowed_books

    def borrow_book(self, book_id):
        """Adds a book ID to the member's borrowed list."""
        if book_id not in self._borrowed_books:
            self._borrowed_books.append(book_id)

    def return_book(self, book_id):
        """Removes a book ID from the member's borrowed list."""
        if book_id in self._borrowed_books:
            self._borrowed_books.remove(book_id)

    def to_dict(self):
        """Converts the Member object to a dictionary."""
        return {
            "member_id": self._member_id,
            "name": self._name,
            "borrowed_books": self._borrowed_books
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Member object from a dictionary."""
        return cls(
            member_id=data["member_id"],
            name=data["name"],
            borrowed_books=data.get("borrowed_books", [])
        )

    def __str__(self):
        return f"[{self._member_id}] {self._name} (Borrowed books: {len(self._borrowed_books)})"
