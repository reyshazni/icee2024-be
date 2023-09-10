from typing import List
from pydantic import BaseModel, EmailStr, Field

class WebinarRegistrationRequest(BaseModel):
    webinar_name: str = Field(..., example="event1")
    full_name: str = Field(..., example="Jeko")
    email: EmailStr = Field(..., example="jeko@icee.com")
    phone_number: str = Field(..., example="08821673463")
    institution: str = Field(..., example="Institut Teknologi Bandung")
    profession: str = Field(..., example="Mahasiswa")
    address: str = Field(..., example="Jalan Gatot Subroto 1A, Jakarta")
    url_bukti_pembayaran: str = Field(..., example="https://foto.jpg/")
