from typing import List
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class CategoryEnum(str, Enum):
    s = "s"
    m = "m"
    l = "l"
    xl = "xl"