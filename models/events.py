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

class EventCategoryEnum(str, Enum):
    seminar = "seminar"
    conference = "conference"
    expo = "expo"

class JenisPesertaEnum(str, Enum):
    umum = "umum"
    tpb = "tpb"
    hms = "hms"

class SumberInfoEnum(str, Enum):
    teman = "teman"
    media_sosial = "media_sosial"
    roadshow = "roadshow"
    website = "website"
    poster = "poster"
    lainnya = "lainnya"

class DataDiriSeminar(BaseModel):
    nama_lengkap: str = Field(..., example="Reinhart Jericho")
    jenis_peserta: JenisPesertaEnum = Field(..., example=JenisPesertaEnum.umum)
    pekerjaan: str = Field(..., example="Software Engineer")
    institusi: str = Field(..., example="PT Teknologi Maju")
    nim: Optional[str] = Field(None, example="18220013")
    alamat: str = Field(..., example="Jl. Merdeka No.10, Jakarta")
    no_telepon: str = Field(..., example="081234567890")
    email: EmailStr = Field(..., example="reinhart@example.com")

    @validator('no_telepon')
    def validate_no_telepon(cls, v):
        if not v.startswith("0"):
            raise ValueError("Nomor telepon harus diawali dengan '0'")
        return v

    @root_validator
    def validate_nim(cls, values):
        jenis_peserta = values.get('jenis_peserta')
        nim = values.get('nim')
        if jenis_peserta != JenisPesertaEnum.umum and not nim:
            raise ValueError("NIM harus diisi untuk jenis peserta adalah mahasiswa ITB")
        return values

class DataDiriConference(BaseModel):
    nama_lengkap: str = Field(..., example="Reinhart Jericho")
    email: EmailStr = Field(..., example="reinhart@example.com")
    no_telepon: str = Field(..., example="081234567890")
    institusi: str = Field(..., example="Institut Teknologi Bandung")
    jurusan: str = Field(..., example="Teknik Sipil")
    alamat: str = Field(..., example="Jl. Merdeka No.10, Jakarta")
    url_ktm: str = Field(..., example="https://storage.googleapis.com/icee24/")

    @validator('no_telepon')
    def validate_no_telepon_conference(cls, v):
        if not v.startswith("0"):
            raise ValueError("Nomor telepon harus diawali dengan '0'")
        return v

class SeminarRequest(BaseModel):
    data_diri: List[DataDiriSeminar]
    url_bukti_pembayaran: str = Field(..., example="https://storage.googleapis.com/icee24/")

class ConferenceRequest(BaseModel):
    data_diri: List[DataDiriConference]
    essay: str = Field(..., example="Kami senang ikut ICEE2024")
    link_submission: str = Field(..., example="https://youtube.com/icee24/")
    kontak_darurat: str = Field(..., example="08123123123")

    @validator('data_diri')
    def validate_data_diri_length(cls, data_diri):
        if len(data_diri) != 3:
            raise ValueError('Tim harus terdiri dari 3 orang')
        return data_diri

class ExpoRequest(BaseModel):
    nama_lengkap: str = Field(..., example="Reinhart Jericho")
    institusi: str = Field(..., example="Institut Teknologi Bandung")
    fakultas: str = Field(..., example="Teknik Sipil")
    nim: str = Field(..., example="18220013")
    sumber_info: SumberInfoEnum = Field(..., example=SumberInfoEnum.website)
    sumber_info_lainnya: Optional[str] = Field(None, example="")
    @validator('sumber_info_lainnya', pre=True, always=True)
    def validate_sumber_info_lainnya(cls, sumber_info_lainnya, values):
        sumber_info = values.get('sumber_info')
        if sumber_info == SumberInfoEnum.lainnya:
            if not sumber_info_lainnya or sumber_info_lainnya.strip() == "":
                raise ValueError('Sumber info lainnya harus diisi jika sumber_info adalah "lainnya"')
        return sumber_info_lainnya