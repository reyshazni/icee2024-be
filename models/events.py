from typing import List
from pydantic import BaseModel, EmailStr, Field

class WebinarRegistrationRequest(BaseModel):
    full_name: str = Field(..., example="John Doe", description="Nama lengkap peserta")
    email: EmailStr = Field(..., example="john@example.com", description="Alamat email peserta")
    phone_number: str = Field(..., example="1234567890", description="Nomor telepon peserta")
    organization: str = Field(..., example="ABC Corp", description="Nama organisasi peserta")
    webinar_id: int = Field(..., example=1, description="ID atau judul webinar")