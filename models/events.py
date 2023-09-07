from typing import List
from pydantic import BaseModel, EmailStr, Field

class WebinarRegistrationRequest(BaseModel):
    full_name: str = Field(..., example="Jeko", description="Nama lengkap peserta")
    email: EmailStr = Field(..., example="jeko@icee.com", description="Alamat email peserta")
    phone_number: str = Field(..., example="08821673463", description="Nomor telepon peserta")
    organization: str = Field(..., example="ICEE ITB", description="Nama organisasi peserta")
    webinar_id: str = Field(..., example="event1", description="ID webinar")
    url_bukti_pembayaran: str = Field(..., example="https://foto.jpg/", description="url")