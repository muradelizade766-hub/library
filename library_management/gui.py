import tkinter as tk
from tkinter import ttk, messagebox
from library import Library

class LibraryApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Library Management System")
        self.window.geometry("1000x740")

        self.is_dark = False

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.apply_theme()

        self.library = Library()

        self.create_widgets()
        self.refresh_books()
        self.refresh_members()
        self.refresh_stats()

    def apply_theme(self):
        if self.is_dark:
            self.bg_color = "black"
            self.fg_color = "white"
            self.btn_color = "gray"
            self.entry_bg = "darkgray"
            self.tree_bg = "black"
            self.tree_fg = "white"
            self.mode_text = "Light Mode"
        else:
            self.bg_color = "darkslategray"
            self.fg_color = "white"
            self.btn_color = "teal"
            self.entry_bg = "white"
            self.tree_bg = "white"
            self.tree_fg = "black"
            self.mode_text = "Dark Mode"

        self.style.configure(".", background=self.bg_color, foreground=self.fg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.fg_color)
        self.style.configure("TButton", background=self.btn_color, foreground=self.fg_color, font=("Arial", 9, "bold"))
        self.style.configure("TLabelframe", background=self.bg_color, foreground=self.fg_color)
        self.style.configure("TLabelframe.Label", background=self.bg_color, foreground=self.fg_color)
        self.style.configure("TNotebook", background=self.bg_color)
        self.style.configure("TNotebook.Tab", background=self.btn_color, foreground=self.fg_color)
        self.style.map("TNotebook.Tab", background=[("selected", "darkcyan" if not self.is_dark else "darkgray")])

        self.style.configure("TEntry", foreground="black", fieldbackground=self.entry_bg)
        self.style.map("TEntry", foreground=[("focus", "black")], fieldbackground=[("focus", self.entry_bg)])

        self.style.configure("Treeview", background=self.tree_bg, fieldbackground=self.tree_bg, foreground=self.tree_fg)
        self.style.configure("Treeview.Heading", background=self.btn_color, foreground=self.fg_color)

        self.window.configure(bg=self.bg_color)

    def toggle_dark_mode(self):
        self.is_dark = not self.is_dark
        self.apply_theme()
        self.mode_btn.config(text=self.mode_text)

    def create_widgets(self):
        top_frame = ttk.Frame(self.window)
        top_frame.pack(fill="x", padx=10, pady=5)

        welcome_label = ttk.Label(
            top_frame, 
            text="Welcome to Library Management System!", 
            font=("Arial", 12, "bold"), 
            foreground="gold"
        )
        welcome_label.pack(side="left", padx=5, pady=5)

        self.mode_btn = ttk.Button(top_frame, text=self.mode_text, command=self.toggle_dark_mode)
        self.mode_btn.pack(side="right", padx=5, pady=5)

        exit_button = ttk.Button(top_frame, text="Exit", command=self.window.destroy, style="Exit.TButton")
        self.style.configure("Exit.TButton", background="darkred", foreground="white")
        exit_button.pack(side="right", padx=5, pady=5)

        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.books_tab = ttk.Frame(notebook)
        notebook.add(self.books_tab, text="Books")

        self.members_tab = ttk.Frame(notebook)
        notebook.add(self.members_tab, text="Members")

        self.borrow_tab = ttk.Frame(notebook)
        notebook.add(self.borrow_tab, text="Borrow / Return")

        self.stats_tab = ttk.Frame(notebook)
        notebook.add(self.stats_tab, text="Statistics")

        self.setup_books_tab()
        self.setup_members_tab()
        self.setup_borrow_tab()
        self.setup_stats_tab()

    def setup_books_tab(self):
        form_frame = ttk.LabelFrame(self.books_tab, text="Add / Edit / Remove Book")
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

        add_button = ttk.Button(form_frame, text="Add Book", command=self.add_book)
        add_button.grid(row=1, column=4, padx=5, pady=5)

        edit_button = ttk.Button(form_frame, text="Edit Selected", command=self.load_selected_book)
        edit_button.grid(row=1, column=5, padx=5, pady=5)

        update_button = ttk.Button(form_frame, text="Update Book", command=self.update_book)
        update_button.grid(row=1, column=6, padx=5, pady=5)

        remove_button = ttk.Button(form_frame, text="Remove Selected", command=self.remove_book)
        remove_button.grid(row=1, column=7, padx=5, pady=5)

        search_frame = ttk.LabelFrame(self.books_tab, text="Search Books")
        search_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5, pady=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        search_button = ttk.Button(search_frame, text="Search", command=self.search_books)
        search_button.pack(side="left", padx=5, pady=5)

        reset_button = ttk.Button(search_frame, text="Reset", command=self.refresh_books)
        reset_button.pack(side="left", padx=5, pady=5)

        sort_frame = ttk.LabelFrame(self.books_tab, text="Sort Books")
        sort_frame.pack(fill="x", padx=10, pady=5)

        sort_title_btn = ttk.Button(sort_frame, text="Title (A-Z)", command=self.sort_by_title)
        sort_title_btn.pack(side="left", padx=5, pady=5)

        sort_author_btn = ttk.Button(sort_frame, text="Author (A-Z)", command=self.sort_by_author)
        sort_author_btn.pack(side="left", padx=5, pady=5)

        sort_year_asc_btn = ttk.Button(sort_frame, text="Year (Asc)", command=self.sort_by_year_asc)
        sort_year_asc_btn.pack(side="left", padx=5, pady=5)

        sort_year_desc_btn = ttk.Button(sort_frame, text="Year (Desc)", command=self.sort_by_year_desc)
        sort_year_desc_btn.pack(side="left", padx=5, pady=5)

        sort_category_btn = ttk.Button(sort_frame, text="Category (A-Z)", command=self.sort_by_category)
        sort_category_btn.pack(side="left", padx=5, pady=5)

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
        form_frame = ttk.LabelFrame(self.members_tab, text="Register / Edit / Remove Member")
        form_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(form_frame, text="Member ID:").grid(row=0, column=0, padx=5, pady=5)
        self.member_id_entry = ttk.Entry(form_frame, width=10)
        self.member_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Name:").grid(row=0, column=2, padx=5, pady=5)
        self.member_name_entry = ttk.Entry(form_frame, width=12)
        self.member_name_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Phone:").grid(row=0, column=4, padx=5, pady=5)
        self.member_phone_entry = ttk.Entry(form_frame, width=12)
        self.member_phone_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(form_frame, text="Email:").grid(row=0, column=6, padx=5, pady=5)
        self.member_email_entry = ttk.Entry(form_frame, width=15)
        self.member_email_entry.grid(row=0, column=7, padx=5, pady=5)

        register_button = ttk.Button(form_frame, text="Register", command=self.register_member)
        register_button.grid(row=1, column=2, padx=5, pady=5)

        edit_button = ttk.Button(form_frame, text="Edit Selected", command=self.load_selected_member)
        edit_button.grid(row=1, column=3, padx=5, pady=5)

        update_button = ttk.Button(form_frame, text="Update Member", command=self.update_member)
        update_button.grid(row=1, column=4, padx=5, pady=5)

        remove_member_button = ttk.Button(form_frame, text="Remove Member", command=self.remove_member)
        remove_member_button.grid(row=1, column=5, padx=5, pady=5)

        self.members_tree = ttk.Treeview(
            self.members_tab, 
            columns=("ID", "Name", "Phone", "Email", "Borrowed Books"), 
            show="headings"
        )
        self.members_tree.heading("ID", text="Member ID")
        self.members_tree.heading("Name", text="Name")
        self.members_tree.heading("Phone", text="Phone")
        self.members_tree.heading("Email", text="Email")
        self.members_tree.heading("Borrowed Books", text="Borrowed Books")

        self.members_tree.column("ID", width=70)
        self.members_tree.column("Name", width=120)
        self.members_tree.column("Phone", width=100)
        self.members_tree.column("Email", width=140)
        self.members_tree.column("Borrowed Books", width=150)

        self.members_tree.pack(fill="both", expand=True, padx=10, pady=5)

    def setup_borrow_tab(self):
        form_frame = ttk.LabelFrame(self.borrow_tab, text="Borrow / Return Operations")
        form_frame.pack(fill="x", padx=10, pady=20)

        ttk.Label(form_frame, text="Member ID:").grid(row=0, column=0, padx=10, pady=10)
        self.borrow_member_id_entry = ttk.Entry(form_frame)
        self.borrow_member_id_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(form_frame, text="Book ID:").grid(row=1, column=0, padx=10, pady=10)
        self.borrow_book_id_entry = ttk.Entry(form_frame)
        self.borrow_book_id_entry.grid(row=1, column=1, padx=10, pady=10)

        borrow_button = ttk.Button(form_frame, text="Borrow Book", command=self.borrow_book)
        borrow_button.grid(row=2, column=0, padx=10, pady=10)

        return_button = ttk.Button(form_frame, text="Return Book", command=self.return_book)
        return_button.grid(row=2, column=1, padx=10, pady=10)

    def setup_stats_tab(self):
        stats_frame = ttk.LabelFrame(self.stats_tab, text="Library Statistics Dashboard")
        stats_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.stat_total_books_lbl = ttk.Label(stats_frame, text="Total books: 0", font=("Arial", 12))
        self.stat_total_books_lbl.pack(anchor="w", padx=20, pady=10)

        self.stat_available_lbl = ttk.Label(stats_frame, text="Available books: 0", font=("Arial", 12))
        self.stat_available_lbl.pack(anchor="w", padx=20, pady=10)

        self.stat_borrowed_lbl = ttk.Label(stats_frame, text="Borrowed books: 0", font=("Arial", 12))
        self.stat_borrowed_lbl.pack(anchor="w", padx=20, pady=10)

        self.stat_members_lbl = ttk.Label(stats_frame, text="Total members: 0", font=("Arial", 12))
        self.stat_members_lbl.pack(anchor="w", padx=20, pady=10)

        self.stat_top_cat_lbl = ttk.Label(stats_frame, text="Top category: N/A", font=("Arial", 12))
        self.stat_top_cat_lbl.pack(anchor="w", padx=20, pady=10)

        refresh_stats_btn = ttk.Button(stats_frame, text="Refresh Statistics", command=self.refresh_stats)
        refresh_stats_btn.pack(anchor="w", padx=20, pady=20)

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
            phone = getattr(member, 'phone', 'N/A')
            email = getattr(member, 'email', 'N/A')
            self.members_tree.insert("", "end", values=(member.member_id, member.name, phone, email, borrowed))

    def refresh_stats(self):
        stats = self.library.get_statistics()
        self.stat_total_books_lbl.config(text=f"Total books: {stats['total_books']}")
        self.stat_available_lbl.config(text=f"Available books: {stats['available_books']}")
        self.stat_borrowed_lbl.config(text=f"Borrowed books: {stats['borrowed_books']}")
        self.stat_members_lbl.config(text=f"Total members: {stats['total_members']}")
        self.stat_top_cat_lbl.config(text=f"Top category: {stats['top_category']}")

    def clear_book_entries(self):
        self.book_id_entry.delete(0, tk.END)
        self.book_title_entry.delete(0, tk.END)
        self.book_author_entry.delete(0, tk.END)
        self.book_year_entry.delete(0, tk.END)
        self.book_category_entry.delete(0, tk.END)

    def clear_member_entries(self):
        self.member_id_entry.delete(0, tk.END)
        self.member_name_entry.delete(0, tk.END)
        self.member_phone_entry.delete(0, tk.END)
        self.member_email_entry.delete(0, tk.END)

    def add_book(self):
        book_id = self.book_id_entry.get().strip()
        title = self.book_title_entry.get().strip()
        author = self.book_author_entry.get().strip()
        year = self.book_year_entry.get().strip()
        category = self.book_category_entry.get().strip()

        if not book_id.isdigit():
            messagebox.showerror("Error", "Book ID must contain only digits!")
            return

        if not year.isdigit():
            messagebox.showerror("Error", "Year must contain only digits!")
            return

        try:
            self.library.add_book(book_id, title, author, year, category)
            messagebox.showinfo("Success", "Book added successfully!")
            self.refresh_books()
            self.refresh_stats()
            self.clear_book_entries()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def load_selected_book(self):
        selected = self.books_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book from the table to edit!")
            return
        
        values = self.books_tree.item(selected[0])["values"]
        self.clear_book_entries()
        self.book_id_entry.insert(0, values[0])
        self.book_title_entry.insert(0, values[1])
        self.book_author_entry.insert(0, values[2])
        self.book_year_entry.insert(0, values[3])
        self.book_category_entry.insert(0, values[4])

    def update_book(self):
        book_id = str(self.book_id_entry.get()).strip()
        if not book_id.isdigit():
            messagebox.showerror("Error", "Book ID must contain only digits!")
            return

        if book_id not in self.library.books:
            messagebox.showerror("Error", "Book ID not found in system!")
            return

        book = self.library.books[book_id]
        book.title = self.book_title_entry.get().strip()
        book.author = self.book_author_entry.get().strip()
        year = self.book_year_entry.get().strip()

        if not year.isdigit():
            messagebox.showerror("Error", "Year must contain only digits!")
            return

        book.year = year
        book.category = self.book_category_entry.get().strip()

        if hasattr(self.library, 'save_data'):
            self.library.save_data()

        messagebox.showinfo("Success", "Book details updated successfully!")
        self.refresh_books()
        self.refresh_stats()
        self.clear_book_entries()

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
            self.refresh_stats()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def search_books(self):
        query = self.search_entry.get()
        results = self.library.search_books(query)
        self.refresh_books(results)

    def sort_by_title(self):
        results = self.library.sort_books_by_title()
        self.refresh_books(results)

    def sort_by_author(self):
        results = self.library.sort_books_by_author()
        self.refresh_books(results)

    def sort_by_year_asc(self):
        results = self.library.sort_books_by_year_asc()
        self.refresh_books(results)

    def sort_by_year_desc(self):
        results = self.library.sort_books_by_year_desc()
        self.refresh_books(results)

    def sort_by_category(self):
        results = self.library.sort_books_by_category()
        self.refresh_books(results)

    def register_member(self):
        member_id = self.member_id_entry.get().strip()
        name = self.member_name_entry.get().strip()
        phone = self.member_phone_entry.get().strip()
        email = self.member_email_entry.get().strip()

        if not member_id.isdigit():
            messagebox.showerror("Error", "Member ID must contain only digits!")
            return

        try:
            try:
                self.library.register_member(member_id, name, phone, email)
            except TypeError:
                self.library.register_member(member_id, name)
                
            messagebox.showinfo("Success", "Member registered successfully!")
            self.refresh_members()
            self.refresh_stats()
            self.clear_member_entries()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def load_selected_member(self):
        selected = self.members_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a member from the table to edit!")
            return

        values = self.members_tree.item(selected[0])["values"]
        self.clear_member_entries()
        self.member_id_entry.insert(0, values[0])
        self.member_name_entry.insert(0, values[1])
        self.member_phone_entry.insert(0, values[2])
        self.member_email_entry.insert(0, values[3])

    def update_member(self):
        member_id = str(self.member_id_entry.get()).strip()
        if not member_id.isdigit():
            messagebox.showerror("Error", "Member ID must contain only digits!")
            return

        if member_id not in self.library.members:
            messagebox.showerror("Error", "Member ID not found in system!")
            return

        member = self.library.members[member_id]
        member.name = self.member_name_entry.get().strip()
        setattr(member, 'phone', self.member_phone_entry.get().strip())
        setattr(member, 'email', self.member_email_entry.get().strip())

        if hasattr(self.library, 'save_data'):
            self.library.save_data()

        messagebox.showinfo("Success", "Member details updated successfully!")
        self.refresh_members()
        self.clear_member_entries()

    def remove_member(self):
        selected_item = self.members_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a member from the list to remove!")
            return

        member_id = self.members_tree.item(selected_item[0])["values"][0]

        try:
            self.library.remove_member(str(member_id))
            messagebox.showinfo("Success", "Member removed successfully!")
            self.refresh_members()
            self.refresh_stats()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def borrow_book(self):
        member_id = self.borrow_member_id_entry.get().strip()
        book_id = self.borrow_book_id_entry.get().strip()

        try:
            self.library.borrow_book(member_id, book_id)
            messagebox.showinfo("Success", "Book borrowed successfully!")
            self.refresh_books()
            self.refresh_members()
            self.refresh_stats()
            self.borrow_member_id_entry.delete(0, tk.END)
            self.borrow_book_id_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def return_book(self):
        member_id = self.borrow_member_id_entry.get().strip()
        book_id = self.borrow_book_id_entry.get().strip()

        try:
            self.library.return_book(member_id, book_id)
            messagebox.showinfo("Success", "Book returned successfully!")
            self.refresh_books()
            self.refresh_members()
            self.refresh_stats()
            self.borrow_member_id_entry.delete(0, tk.END)
            self.borrow_book_id_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
