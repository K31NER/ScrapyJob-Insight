from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class Senioriry(str, Enum):
    Senior = "Senior"
    Mid = "Mid"
    Junior = "Junior"
    Entry = "Entry"
    
class JobsProcces(BaseModel):
    """Modelo para proccesar un job y extraer la informacion relevante."""
    
    skills: List[str] = Field(...,description="Tecnologias que reconoces del texto. ejemplo: [python,sql]" )
    location: str = Field(...,description="Pais de la oferta donde se define usando el codigo de pais. Ejemplo: CO, US, MX etc")
    seniority: Senioriry = Field(...,description="Nivel de experiencia requerido por la vacante. Ejemplo: Junior")
    
class JobEntry(BaseModel):
    title: str
    location: Optional[str]
    description: str