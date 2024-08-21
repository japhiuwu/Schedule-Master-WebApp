from pydantic import BaseModel, validator
from typing import Optional
import re

from utils.globalf import validate_sql_injection

class UserRegister(BaseModel):
    Id_Usuario: str
    Email: str
    Password: str
    Primer_Nombre: str
    Segundo_Nombre: Optional[str] = None
    Primer_Apellido: str
    Segundo_Apellido: Optional[str] = None
    Foto_Perfil: Optional[str] = None

    @validator('Password')
    def password_validation(cls, value):
        if len(value) < 6:
            raise ValueError('Password must be at least 6 characters long')

        if not re.search(r'[A-Z]', value):
            raise ValueError('Password must contain at least one uppercase letter')

        if not re.search(r'[\W_]', value):
            raise ValueError('Password must contain at least one special character')

        if re.search(r'(012|123|234|345|456|567|678|789|890)', value):
            raise ValueError('Password must not contain a sequence of numbers')

        return value

    @validator('Primer_Nombre', 'Segundo_Nombre', 'Primer_Apellido', 'Segundo_Apellido')
    def name_validation(cls, value):
        if validate_sql_injection(value):
            raise ValueError('Invalid name')

        return value
    
    @validator('Email')
    def email_validation(cls, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError('Invalid email address')

        return value
