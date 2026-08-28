from models import Book, Member

class Library:
    def __init__(self, books_file="data/books.txt", members_file="data/members.txt"):
        self.books_file = books_file
        self.members_file = members_file
        self.books = {}
        self.members = {}

        self.load_data()

    def load_data(self):
        try:
            with open(self.books_file, "r", encoding="utf-8") as file:
                for line in file:
                    book = Book.from_file_string(line)
                    if book:
                        self.books[book.book_id] = book
        except FileNotFoundError:
            pass

        try:
            with open(self.members_file, "r", encoding="utf-8") as file:
                for line in file:
                    member = Member.from_file_string(line)
                    if member:
                        self.members[member.member_id] = member
        except FileNotFoundError:
            pass

    def save_books(self):
        with open(self.books_file, "w", encoding="utf-8") as file:
            for book in self.books.values():
                file.write(book.to_file_string())

    def save_members(self):
        with open(self.members_file, "w", encoding="utf-8") as file:
            for member in self.members.values():
                file.write(member.to_file_string())

    def add_book(self, book_id, title, author, year="", category=""):
        if not book_id or not title or not author:
            raise ValueError("Book ID, Title, and Author are required!")
        if str(book_id) in self.books:
            raise ValueError("Book ID already exists!")

        new_book = Book(book_id, title, author, year, category)
        self.books[str(book_id)] = new_book
        self.save_books()

    def remove_book(self, book_id):
        book_id = str(book_id)
        if book_id not in self.books:
            raise ValueError("Book not found!")
        if self.books[book_id].is_borrowed:
            raise ValueError("Cannot remove a borrowed book!")

        del self.books[book_id]
        self.save_books()

    def search_books(self, query):
        query = query.lower()
        results = []
        for book in self.books.values():
            if (query in book.title.lower() or 
                query in book.author.lower() or 
                query in book.book_id.lower() or 
                query in book.category.lower()):
                results.append(book)
        return results

    def register_member(self, member_id, name):
        member_id = str(member_id)
        if not member_id or not name:
            raise ValueError("Member ID and Name are required!")
        if member_id in self.members:
            raise ValueError("Member ID already exists!")

        new_member = Member(member_id, name)
        self.members[member_id] = new_member
        self.save_members()

    def borrow_book(self, member_id, book_id):
        member_id = str(member_id)
        book_id = str(book_id)

        if member_id not in self.members:
            raise ValueError("Member not found!")
        if book_id not in self.books:
            raise ValueError("Book not found!")

        book = self.books[book_id]
        member = self.members[member_id]

        if book.is_borrowed:
            raise ValueError("Book is already borrowed!")

        book.is_borrowed = True
        member.borrow_book(book_id)

        self.save_books()
        self.save_members()

    def return_book(self, member_id, book_id):
        member_id = str(member_id)
        book_id = str(book_id)

        if member_id not in self.members:
            raise ValueError("Member not found!")
        if book_id not in self.books:
            raise ValueError("Book not found!")

        book = self.books[book_id]
        member = self.members[member_id]

        if not book.is_borrowed:
            raise ValueError("Book was not borrowed!")

        book.is_borrowed = False
        member.return_book(book_id)

        self.save_books()
        self.save_members()
