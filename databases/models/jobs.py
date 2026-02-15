from datetime import date
from typing import Optional
from utils.procces_page import Page
from pydantic import BaseModel, Field

class Jobs(BaseModel):
    title: str
    page: Page
    link: str
    salary: str
    location: str
    description: str
    skills: Optional[list[str]] = None
    seniority: Optional[str] = None
    search_date: Optional[date] = Field(default_factory=date.today)
    
    model_config = {
        "use_enum_values": True
    }
