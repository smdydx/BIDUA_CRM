
"""
Custom exception classes for database operations and validations
"""

class DatabaseError(Exception):
    """Base database exception"""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ValidationError(DatabaseError):
    """Validation error exception"""
    def __init__(self, field: str, message: str, value=None):
        self.field = field
        self.value = value
        super().__init__(f"Validation error in field '{field}': {message}", "VALIDATION_ERROR")


class DuplicateEntryError(DatabaseError):
    """Duplicate entry exception"""
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"Duplicate entry '{value}' for field '{field}'", "DUPLICATE_ENTRY")


class NotFoundError(DatabaseError):
    """Record not found exception"""
    def __init__(self, model: str, identifier: str):
        self.model = model
        self.identifier = identifier
        super().__init__(f"{model} with ID '{identifier}' not found", "NOT_FOUND")


class ForeignKeyError(DatabaseError):
    """Foreign key constraint exception"""
    def __init__(self, field: str, value: str, reference_table: str):
        self.field = field
        self.value = value
        self.reference_table = reference_table
        super().__init__(f"Foreign key constraint failed: {field}='{value}' not found in {reference_table}", "FOREIGN_KEY_ERROR")


class BusinessLogicError(DatabaseError):
    """Business logic violation exception"""
    def __init__(self, message: str):
        super().__init__(f"Business logic error: {message}", "BUSINESS_LOGIC_ERROR")


class PermissionError(DatabaseError):
    """Permission denied exception"""
    def __init__(self, action: str, resource: str):
        self.action = action
        self.resource = resource
        super().__init__(f"Permission denied: Cannot {action} {resource}", "PERMISSION_DENIED")


class DataIntegrityError(DatabaseError):
    """Data integrity constraint exception"""
    def __init__(self, constraint: str, message: str):
        self.constraint = constraint
        super().__init__(f"Data integrity error ({constraint}): {message}", "DATA_INTEGRITY_ERROR")
