from typing import List
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class NonWorkshopEnum(str, Enum):
    conference = "conference"
    expo = "expo"
    seminar = "seminar"

class FileTypeEnum(str, Enum):
    bukti_pembayaran = "bukti_pembayaran"
    bukti_follow = "bukti_follow"
    ktm = "ktm"

class NonWorkshopRegistrationRequest(BaseModel):
    event_name: str = Field(..., example="event1")
    full_name: NonWorkshopEnum = Field(..., example="conference")
    email: EmailStr = Field(..., example="jeko@icee.com")
    phone_number: str = Field(..., example="08821673463")
    institution: str = Field(..., example="Institut Teknologi Bandung")
    profession: str = Field(..., example="Mahasiswa")
    address: str = Field(..., example="Jalan Gatot Subroto 1A, Jakarta")
    url_bukti_pembayaran: str = Field(..., example="https://storage.googleapis.com/bucket/file.jpg")

class WorkshopRegistrationRequest(BaseModel):
    full_name: str = Field(..., example="Jeko")
    email: EmailStr = Field(..., example="jeko@icee.com")
    phone_number: str = Field(..., example="08821673463")
    institution: str = Field(..., example="Institut Teknologi Bandung")
    profession: str = Field(..., example="Mahasiswa")
    address: str = Field(..., example="Jalan Gatot Subroto 1A, Jakarta")
    url_bukti_follow: str = Field(..., example="https://storage.googleapis.com/bucket/file.jpg")
