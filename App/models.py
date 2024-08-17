from pydantic import BaseModel, Field
from typing import Optional


class Usuario(BaseModel):
    nombre: str
    edad: int = Field(..., ge=0, description="Edad debe ser un valor positivo")
    email: Optional[str] = None
