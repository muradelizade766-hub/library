class FileManager:
  """Class responsible for saving and loading data to/from text files."""

  @staticmethod
  def save_to_text(file_path, lines):
    """Saves a list of text lines to a file."""
    with open(file_path, "w", encoding = "utf-8") as file:
      for line in lines:
        file.write(f"{line}\n")

  @staticmethod
  def load_from_text(file_path):
    """Loads text lines from a file. Returns empty list if file does not exist."""
    try:
      with open(file_path, "r", encoding = "utf-8") as file:
        return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
      return []
      
      
