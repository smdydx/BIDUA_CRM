
"""
Validation utility functions for the CRM-HRMS system
"""
import re
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, Union


class ValidationError(Exception):
    """Custom validation error"""
    pass


def validate_email(email: str) -> str:
    """Validate email format"""
    if not email:
        raise ValidationError("Email is required")
    
    email = email.strip().lower()
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    if not email_pattern.match(email):
        raise ValidationError("Invalid email format")
    
    return email


def validate_phone(phone: str) -> str:
    """Validate phone number format"""
    if not phone:
        return phone
    
    # Remove all non-digit characters for validation
    digits_only = re.sub(r'\D', '', phone)
    
    if len(digits_only) < 10 or len(digits_only) > 15:
        raise ValidationError("Phone number must be between 10-15 digits")
    
    return phone


def validate_indian_pan(pan: str) -> str:
    """Validate Indian PAN number format"""
    if not pan:
        return pan
    
    pan = pan.upper().strip()
    pan_pattern = re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$')
    
    if not pan_pattern.match(pan):
        raise ValidationError("Invalid PAN number format. Format: ABCDE1234F")
    
    return pan


def validate_indian_gst(gst: str) -> str:
    """Validate Indian GST number format"""
    if not gst:
        return gst
    
    gst = gst.upper().strip()
    # GST format: 2 digits (state) + 10 digits (PAN) + 1 digit + 1 letter + 1 digit
    gst_pattern = re.compile(r'^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$')
    
    if not gst_pattern.match(gst):
        raise ValidationError("Invalid GST number format")
    
    return gst


def validate_indian_aadhar(aadhar: str) -> str:
    """Validate Indian Aadhar number format"""
    if not aadhar:
        return aadhar
    
    # Remove spaces and validate 12 digits
    aadhar_clean = re.sub(r'\s', '', aadhar)
    
    if not re.match(r'^\d{12}$', aadhar_clean):
        raise ValidationError("Aadhar number must be 12 digits")
    
    return aadhar_clean


def validate_ifsc_code(ifsc: str) -> str:
    """Validate Indian IFSC code format"""
    if not ifsc:
        return ifsc
    
    ifsc = ifsc.upper().strip()
    # IFSC format: 4 letters + 7 alphanumeric
    ifsc_pattern = re.compile(r'^[A-Z]{4}[A-Z0-9]{7}$')
    
    if not ifsc_pattern.match(ifsc):
        raise ValidationError("Invalid IFSC code format. Format: ABCD0123456")
    
    return ifsc


def validate_url(url: str) -> str:
    """Validate URL format"""
    if not url:
        return url
    
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(url):
        raise ValidationError("Invalid URL format")
    
    return url


def validate_positive_decimal(value: Union[Decimal, float, int], field_name: str) -> Union[Decimal, float, int]:
    """Validate positive decimal/numeric values"""
    if value is None:
        return value
    
    if value < 0:
        raise ValidationError(f"{field_name} cannot be negative")
    
    return value


def validate_percentage(value: int, field_name: str) -> int:
    """Validate percentage values (0-100)"""
    if value is None:
        return value
    
    if value < 0 or value > 100:
        raise ValidationError(f"{field_name} must be between 0 and 100")
    
    return value


def validate_date_range(start_date: date, end_date: date, field_prefix: str = "") -> tuple:
    """Validate date range (end >= start)"""
    if start_date and end_date:
        if end_date < start_date:
            raise ValidationError(f"{field_prefix}End date cannot be before start date")
    
    return start_date, end_date


def validate_future_date(date_value: date, field_name: str, allow_today: bool = True) -> date:
    """Validate that date is in future (or today if allowed)"""
    if not date_value:
        return date_value
    
    today = date.today()
    
    if allow_today:
        if date_value < today:
            raise ValidationError(f"{field_name} cannot be in the past")
    else:
        if date_value <= today:
            raise ValidationError(f"{field_name} must be in the future")
    
    return date_value


def validate_age_range(birth_date: date, min_age: int = 18, max_age: int = 100) -> date:
    """Validate age range based on birth date"""
    if not birth_date:
        return birth_date
    
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    if age < min_age or age > max_age:
        raise ValidationError(f"Age must be between {min_age} and {max_age} years")
    
    return birth_date


def validate_string_length(value: str, field_name: str, min_length: int = 1, max_length: int = None) -> str:
    """Validate string length"""
    if not value:
        if min_length > 0:
            raise ValidationError(f"{field_name} is required")
        return value
    
    value = value.strip()
    
    if len(value) < min_length:
        raise ValidationError(f"{field_name} must be at least {min_length} characters long")
    
    if max_length and len(value) > max_length:
        raise ValidationError(f"{field_name} cannot be more than {max_length} characters long")
    
    return value


def validate_employee_id_format(employee_id: str) -> str:
    """Validate employee ID format (EMP001, EMP002, etc.)"""
    if not employee_id:
        raise ValidationError("Employee ID is required")
    
    employee_id = employee_id.upper().strip()
    
    if not re.match(r'^EMP\d{3,6}$', employee_id):
        raise ValidationError("Employee ID must be in format EMP001, EMP002, etc.")
    
    return employee_id


def validate_currency_amount(amount: Union[Decimal, float], field_name: str, max_amount: Union[Decimal, float] = None) -> Union[Decimal, float]:
    """Validate currency amounts"""
    if amount is None:
        raise ValidationError(f"{field_name} is required")
    
    if amount <= 0:
        raise ValidationError(f"{field_name} must be positive")
    
    if max_amount and amount > max_amount:
        raise ValidationError(f"{field_name} cannot exceed {max_amount}")
    
    return amount
