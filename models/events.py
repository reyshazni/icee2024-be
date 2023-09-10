from typing import List
from pydantic import BaseModel, EmailStr, Field

class WebinarRegistrationRequest(BaseModel):
    webinar_name: str = Field(..., example="event1", description="ID webinar")
    full_name: str = Field(..., example="Jeko", description="Nama lengkap peserta")
    email: EmailStr = Field(..., example="jeko@icee.com", description="Alamat email peserta")
    phone_number: str = Field(..., example="08821673463", description="Nomor telepon peserta")
    institution: str = Field(..., example="Institut Teknologi Bandung", description="Nama instititusi peserta")
    profession: str = Field(..., example="Mahasiswa", description="Nama organisasi peserta")
    address: str = Field(..., example="Jalan Gatot Subroto 1A, Jakarta", description="Alamat")
    url_bukti_pembayaran: str = Field(..., example="https://foto.jpg/", description="url")