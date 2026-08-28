import tkinter as tk
from tkinter import ttk, messagebox
from library import Library

class LibraryApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Library Management System")
        self.window.geometry("900x650")

        style = ttk.Style()
        style.theme_use('clam')

        bg_color = "navy"
        fg_color = "white"
        btn_color = "steelblue"

        style.configure(".", background=bg_color, foreground=fg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color)
        style.configure("TButton", background=btn_color, foreground=fg_color, font=("Arial", 9, "bold"))
        style.configure("TLabelframe", background=bg_color, foreground=fg_color)
        style.configure("TLabelframe.Label", background=bg_color, foreground=fg_color)
        style.configure("TNotebook", background=bg_color)
        style.configure("TNotebook.Tab", background=btn_color, foreground=fg_color)
        style.map("TNotebook.Tab", background=[("selected", "blue")])
        style.configure("Treeview", background="white", fieldbackground="white", foreground="black")
        style.configure("Treeview.Heading", background=btn_color, foreground=fg_color)

        self.window.configure(bg=bg_color)

        self.library = Library()

        self.create_widgets()
        self.refresh_books()
        self.refresh_members()

    def create_widgets(self):
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.books_tab = ttk.Frame(notebook)
        notebook.add(self.books_tab, text="Books")

        self.members_tab = ttk.Frame(notebook)
        notebook.add(self.members_tab, text="Members")

        self.borrow_tab = ttk.Frame(notebook)
        notebook.add(self.borrow_tab, text="Borrow / Return")

        self.setup_books_tab()
        self.setup_members_tab()
        self.setup_borrow_tab()

    def setup_books_tab(self):
        form_frame = ttk.LabelFrame(self.books_tab, text="Add / Remove Book")
        form_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(form_frame, text="Book ID:").grid(row=0, column=0, padx=5, pady=5)
        self.book_id_entry = ttk.Entry(form_frame, width=12)
        self.book_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Title:").grid(row=0, column=2, padx=5, pady=5)
        self.book_title_entry = ttk.Entry(form_frame, width=15)
        self.book_title_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Author:").grid(row=0, column=4, padx=5, pady=5)
        self.book_author_entry = ttk.Entry(form_frame, width=15)
        self.book_author_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(form_frame, text="Year:").grid(row=1, column=0, padx=5, pady=5)
        self.book_year_entry = ttk.Entry(form_frame, width=12)
        self.book_year_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Category:").grid(row=1, column=2, padx=5, pady=5)
        self.book_category_entry = ttk.Entry(form_frame, width=15)
        self.book_category_entry.grid(row=1, column=3, padx=5, pady=5)

        button = ttk.Button(form_frame, text="Add Book", command=self.add_book)
        button.grid(row=1, column=4, padx=5, pady=5)

        remove_button = ttk.Button(form_frame, text="Remove Selected", command=self.remove_book)
        remove_button.grid(row=1, column=5, padx=5, pady=5)

        search_frame = ttk.LabelFrame(self.books_tab, text="Search Books")
        search_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5, pady=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        search_button = ttk.Button(search_frame, text="Search", command=self.search_books)
        search_button.pack(side="left", padx=5, pady=5)

        reset_button = ttk.Button(search_frame, text="Reset", command=self.refresh_books)
        reset_button.pack(side="left", padx=5, pady=5)

        self.books_tree = ttk.Treeview(
            self.books_tab, 
            columns=("ID", "Title", "Author", "Year", "Category", "Status"), 
            show="headings"
        )
        self.books_tree.heading("ID", text="Book ID")
        self.books_tree.heading("Title", text="Title")
        self.books_tree.heading("Author", text="Author")
        self.books_tree.heading("Year", text="Year")
        self.books_tree.heading("Category", text="Category")
        self.books_tree.heading("Status", text="Status")

        self.books_tree.column("ID", width=70)
        self.books_tree.column("Title", width=150)
        self.books_tree.column("Author", width=120)
        self.books_tree.column("Year", width=60)
        self.books_tree.column("Category", width=100)
        self.books_tree.column("Status", width=90)

        self.books_tree.pack(fill="both", expand=True, padx=10, pady=5)

    def setup_members_tab(self):
        form_frame = ttk.LabelFrame(self.members_tab, text="Register Member")
        form_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(form_frame, text="Member ID:").grid(row=0, column=0, padx=5, pady=5)
        self.member_id_entry = ttk.Entry(form_frame)
        self.member_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Name:").grid(row=0, column=2, padx=5, pady=5)
        self.member_name_entry = ttk.Entry(form_frame)
        self.member_name_entry.grid(row=0, column=3, padx=5, pady=5)

        register_button = ttk.Button(form_frame, text="Register Member", command=self.register_member)
        register_button.grid(row=0, column=4, padx=5, pady=5)

        self.members_tree = ttk.Treeview(self.members_tab, columns=("ID", "Name", "Borrowed Books"), show="headings")
        self.members_tree.heading("ID", text="Member ID")
        self.members_tree.heading("Name", text="Name")
        self.members_tree.heading("Borrowed Books", text="Borrowed Books")
        self.members_tree.pack(fill="both", expand=True, padx=10, pady=5)

    def setup_borrow_tab(self):
        form_frame = ttk.LabelFrame(self.borrow_tab, text="Borrow / Return Operations")
        form_frame.pack(fill="x", padx=10, pady=20)

        ttk.Label(form_frame, text="Member ID:").grid(row=0, column=0, padx=10, pady=10)
        self.op_member_id_entry = ttk.Entry(form_frame)
        self.op_member_id_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(form_frame, text="Book ID:").grid(row=1, column=0, padx=10, pady=10)
        self.op_book_id_entry = ttk.Entry(form_frame)
        self.op_book_id_entry.grid(row=1, column=1, padx=10, pady=10)

        borrow_button = ttk.Button(form_frame, text="Borrow Book", command=self.borrow_book)
        borrow_button.grid(row=2, column=0, padx=10, pady=10)

        return_button = ttk.Button(form_frame, text="Return Book", command=self.return_book)
        return_button.grid(row=2, column=1, padx=10, pady=10)

    def refresh_books(self, book_list=None):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)

        books = book_list if book_list is not None else self.library.books.values()
        for book in books:
            status = "Borrowed" if book.is_borrowed else "Available"
            self.books_tree.insert(
                "", "end", 
                values=(book.book_id, book.title, book.author, book.year, book.category, status)
            )

    def refresh_members(self):
        for item in self.members_tree.get_children():
            self.members_tree.delete(item)

        for member in self.library.members.values():
            borrowed = ", ".join(member.borrowed_books) if member.borrowed_books else "None"
            self.members_tree.insert("", "end", values=(member.member_id, member.name, borrowed))

    def add_book(self):
        book_id = self.book_id_entry.get()
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()
        year = self.book_year_entry.get()
        category = self.book_category_entry.get()

        try:
            self.library.add_book(book_id, title, author, year, category)
            messagebox.showinfo("Success", "Book added successfully!")
            self.refresh_books()
            self.book_id_entry.delete(0, tk.END)
            self.book_title_entry.delete(0, tk.END)
            self.book_author_entry.delete(0, tk.END)
            self.book_year_entry.delete(0, tk.END)
            self.book_category_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def remove_book(self):
        selected_item = self.books_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a book from the list to remove!")
            return

        book_id = self.books_tree.item(selected_item[0])["values"][0]

        try:
            self.library.remove_book(str(book_id))
            messagebox.showinfo("Success", "Book removed successfully!")
            self.refresh_books()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def search_books(self):
        query = self.search_entry.get()
        results = self.library.search_books(query)
        self.refresh_books(results)

    def register_member(self):
        member_id = self.member_id_entry.get()
        name = self.member_name_entry.get()

        try:
            self.library.register_member(member_id, name)
            messagebox.showinfo("Success", "Member registered successfully!")
            self.refresh_members()
            self.member_id_entry.delete(0, tk.END)
            self.member_name_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def borrow_book(self):
        member_id = self.op_member_id_entry.get()
        book_id = self.op_book_id_entry.get()

        try:
            self.library.borrow_book(member_id, book_id)
            messagebox.showinfo("Success", "Book borrowed successfully!")
            self.refresh_books()
            self.refresh_members()
            self.op_member_id_entry.delete(0, tk.END)
            self.op_book_id_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def return_book(self):
        member_id = self.op_member_id_entry.get()
        book_id = self.op_book_id_entry.get()

        try:
            self.library.return_book(member_id, book_id)
            messagebox.showinfo("Success", "Book returned successfully!")
            self.refresh_books()
            self.refresh_members()
            self.op_member_id_entry.delete(0, tk.END)
            self.op_book_id_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
