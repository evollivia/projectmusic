from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.model.base import Base


# 게시판 테이블
class Board(Base):
    __tablename__ = 'board'

    bno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    userid: Mapped[str] = mapped_column(ForeignKey('member.userid'), index=True) # Member의 userid
    regdate: Mapped[datetime] = mapped_column(default=datetime.now)
    views: Mapped[int] = mapped_column(default=0)
    contents: Mapped[str]

# 게시판 파일업로드 테이블
class BoardFile(Base):
    __tablename__ = 'boardfile'
    fno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    bno: Mapped[int] = mapped_column(ForeignKey('board.bno'), index=True)
    fname: Mapped[str] = mapped_column(nullable=False)
    fsize: Mapped[int] = mapped_column(default=0)
    regdate: Mapped[datetime] = mapped_column(default=datetime.now)

# 게시판 댓글
# class Reply(Base):
#     __tablename__ = 'reply'
#
#     reply_no: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
#     bno: Mapped[int] = mapped_column(ForeignKey('board.board_no')) # board의 board_no
#     reply_writer: Mapped[str]
#     reply_ment: Mapped[str]
#     reply_date: Mapped[datetime] = mapped_column(default=datetime.now)