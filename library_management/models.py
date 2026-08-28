class Book:
    def __init__(self, book_id, title, author, year="", category="", is_borrowed=False):
        self.book_id = str(book_id)
        self.title = title
        self.author = author
        self.year = str(year)
        self.category = category
        self.is_borrowed = is_borrowed

    def to_file_string(self):
        return f"{self.book_id}|{self.title}|{self.author}|{self.year}|{self.category}|{self.is_borrowed}\n"

    @classmethod
    def from_file_string(cls, file_string):
        parts = file_string.strip().split("|")
        if len(parts) >= 6:
            return cls(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5] == "True")
        elif len(parts) == 4:
            return cls(parts[0], parts[1], parts[2], "", "", parts[3] == "True")
        return None


class Member:
    def __init__(self, member_id, name, borrowed_books=None):
        self.member_id = str(member_id)
        self.name = name
        self.borrowed_books = borrowed_books if borrowed_books is not None else []

    def borrow_book(self, book_id):
        if str(book_id) not in self.borrowed_books:
            self.borrowed_books.append(str(book_id))

    def return_book(self, book_id):
        if str(book_id) in self.borrowed_books:
            self.borrowed_books.remove(str(book_id))

    def to_file_string(self):
        books_str = ",".join(self.borrowed_books)
        return f"{self.member_id}|{self.name}|{books_str}\n"

    @classmethod
    def from_file_string(cls, file_string):
        parts = file_string.strip().split("|")
        if len(parts) >= 2:
            borrowed = parts[2].split(",") if len(parts) > 2 and parts[2] else []
            return cls(parts[0], parts[1], borrowed)
        return None
