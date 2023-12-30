from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, validator, root_validator
from enum import Enum

class NonWorkshopEnum(str, Enum):
    conference = "conference"
    expo = "expo"
    seminar = "seminar"

class FileTypeEnum(str, Enum):
    bukti_pembayaran = "bukti_pembayaran"
    bukti_follow = "bukti_follow"
    ktm = "ktm"

class JenisPesertaEnum(str, Enum):
    umum = "umum"
    tpb = "tpb"
    hms = "hms"

class DataDiri(BaseModel):
    nama_lengkap: str = Field(..., example="Reinhart Jericho")
    jenis_peserta: JenisPesertaEnum = Field(..., example=JenisPesertaEnum.umum)
    pekerjaan: str = Field(..., example="Software Engineer")
    institusi: str = Field(..., example="PT Teknologi Maju")
    nim: Optional[str] = Field(None, example="12345678")
    alamat: str = Field(..., example="Jl. Merdeka No.10, Jakarta")
    no_telp: str = Field(..., example="081234567890")
    email: EmailStr = Field(..., example="reinhart@example.com")

    @validator('no_telp')
    def validate_no_telp(cls, v):
        if not v.startswith("0"):
            raise ValueError("Nomor telepon harus diawali dengan '0'")
        return v

    @root_validator
    def validate_nim(cls, values):
        jenis_peserta = values.get('jenis_peserta')
        nim = values.get('nim')
        if jenis_peserta != JenisPesertaEnum.umum and not nim:
            raise ValueError("NIM harus diisi untuk jenis peserta selain 'umum'")
        return values

class SeminarRequest(BaseModel):
    data_diri: List[DataDiri]
    url_bukti_pembayaran: str = Field(..., example="https://storage.googleapis.com/bucket/file.jpg")