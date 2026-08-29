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

    def sort_books_by_title(self):
        return sorted(self.books.values(), key=lambda b: b.title.lower())

    def sort_books_by_author(self):
        return sorted(self.books.values(), key=lambda b: b.author.lower())

    def sort_books_by_year_asc(self):
        return sorted(self.books.values(), key=lambda b: int(b.year) if str(b.year).isdigit() else 0)

    def sort_books_by_year_desc(self):
        return sorted(self.books.values(), key=lambda b: int(b.year) if str(b.year).isdigit() else 0, reverse=True)

    def sort_books_by_category(self):
        return sorted(self.books.values(), key=lambda b: b.category.lower())

    def register_member(self, member_id, name, phone="", email=""):
        member_id = str(member_id)
        if not member_id or not name:
            raise ValueError("Member ID and Name are required!")
        if member_id in self.members:
            raise ValueError("Member ID already exists!")

        try:
            new_member = Member(member_id, name, phone, email)
        except TypeError:
            new_member = Member(member_id, name)
            if hasattr(new_member, 'phone'):
                new_member.phone = phone
            if hasattr(new_member, 'email'):
                new_member.email = email
            
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

        if hasattr(member, 'borrowed_books') and book_id not in member.borrowed_books:
            raise ValueError("This member did not borrow this book!")

        book.is_borrowed = False
        member.return_book(book_id)

        self.save_books()
        self.save_members()

    def get_statistics(self):
        total_books = len(self.books)
        borrowed_books = sum(1 for book in self.books.values() if book.is_borrowed)
        available_books = total_books - borrowed_books
        total_members = len(self.members)

        category_counts = {}
        for book in self.books.values():
            cat = book.category.strip() if book.category else "Uncategorized"
            category_counts[cat] = category_counts.get(cat, 0) + 1

        if category_counts:
            top_category = max(category_counts, key=category_counts.get)
            top_count = category_counts[top_category]
            top_category_text = f"{top_category} ({top_count} books)"
        else:
            top_category_text = "N/A"

        return {
            "total_books": total_books,
            "available_books": available_books,
            "borrowed_books": borrowed_books,
            "total_members": total_members,
            "top_category": top_category_text
        }
