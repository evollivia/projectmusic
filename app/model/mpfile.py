from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.model.base import Base


class Mpfile(Base):
    __tablename__ = 'mpfile'

    mno: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    genre: Mapped[str] = mapped_column(String, index=True)
    country: Mapped[str] = mapped_column(String, index=True)
    mp3_path: Mapped[str] = mapped_column(String, index=True)  # .mp3 파일의 경로를 저장할 컬럼 추가
    img_path: Mapped[str] = mapped_column(String, index=True)  # .mp3 파일의 경로를 저장할 컬럼 추가


