from typing import List
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class NonWorkshopEnum(str, Enum):
    conference = "conference"
    expo = "expo"
    seminar = "seminar"

class WorkshopEnum(str, Enum):
    workshop_1 = "workshop_1"
    workshop_2 = "workshop_2"

class FileTypeEnum(str, Enum):
    bukti_pembayaran = "bukti_pembayaran"
    bukti_follow = "bukti_follow"

class NonWorkshopRegistrationRequest(BaseModel):
    event_name: str = Field(..., example="event1")
    full_name: NonWorkshopEnum = Field(..., example="conference")
    email: EmailStr = Field(..., example="jeko@icee.com")
    phone_number: str = Field(..., example="08821673463")
    institution: str = Field(..., example="Institut Teknologi Bandung")
    profession: str = Field(..., example="Mahasiswa")
    address: str = Field(..., example="Jalan Gatot Subroto 1A, Jakarta")
    url_bukti_pembayaran: str = Field(..., example="https://buktibayarjpg.jpg/")

class WorkshopRegistrationRequest(BaseModel):
    event_name: WorkshopEnum = Field(..., example="workshop_1")
    full_name: str = Field(..., example="Jeko")
    email: EmailStr = Field(..., example="jeko@icee.com")
    phone_number: str = Field(..., example="08821673463")
    institution: str = Field(..., example="Institut Teknologi Bandung")
    profession: str = Field(..., example="Mahasiswa")
    address: str = Field(..., example="Jalan Gatot Subroto 1A, Jakarta")
    url_bukti_follow: str = Field(..., example="https://buktifollow.jpg/")
