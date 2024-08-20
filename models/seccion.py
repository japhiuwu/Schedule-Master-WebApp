from pydantic import BaseModel, validator
from typing import Optional

class seccion(BaseModel):
    Cod_Periodo: str
    Cod_Carrera: str
    Cod_Clase: int
    Cod_Seccion: int
    Cod_Edificio: str
    Num_Aula: int
    Num_Empleado: str
    Cupos: int
    Dias: str
    Hora_Inicial: str
    Hora_Final: str
    Portada: str

    @validator('Cod_Periodo', 'Cod_Carrera', 'Cod_Edificio', 'Num_Empleado')
    def no_empty(cls, v):
        if not v:
            raise ValueError(f'{v} cannot be empty')
        return v

    @validator('Hora_Final')
    def hora_final_must_be_greater_than_hora_inicial(cls, v, values):
        if 'Hora_Inicial' in values and v <= values['Hora_Inicial']:
            raise ValueError('Hora_Final must be greater than Hora_Inicial')
        return v

    @validator('Portada', always=True)
    def validate_portada(cls, v):
        # Permitir None o una cadena vacía
        if v is not None and len(v) < 0:
            raise ValueError('Portada cannot be an empty string if provided')
        return v

    class Config:
        str_strip_whitespace = True
