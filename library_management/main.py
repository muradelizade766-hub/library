import tkinter as tk
from gui import LibraryApp

def main():
  window = tk.Tk()
  app = LibraryApp(window)
  window.mainloop()


if __name__ == "__main__":
  main()
