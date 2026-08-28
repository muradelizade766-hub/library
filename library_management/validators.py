class Validator:
  """Utility class for validating user input data"""

@staticmethod
def validate_not_empty(value, field_name):
  """Ensures that string input is not or whitespace"""
  if not value or not str(value).strip():
    raise ValueError(f"{field_name} cannot be empty!")
    return str(value).strip()

@staticmethod
def validate_id(id_value, entity_type = "ID"):
  """Ensures that ID is provided and formatted properly"""
  clean_id = Validator.validate_not_empty(id_value, entity_type)
  if len(clean_id) < 1:
        raise ValueError(f"Invalid {entity_type}! It must contain at least 1 character!")
        return clean_id
