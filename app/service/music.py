from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.model.mpfile import Mpfile

class MusicService:
    @staticmethod
    def select_music(db):
        try:
            # 페이지당 항목 수
            items_per_page = 10

            # SQL 쿼리 작성
            stmt = select(Mpfile.name, Mpfile.title).limit(items_per_page)

            # 쿼리 실행 및 결과 반환
            result = db.execute(stmt)
            return result.fetchall()  # Row 객체의 리스트를 반환

        except SQLAlchemyError as ex:
            print(f'▶▶▶ select_music 오류발생 : {str(ex)}')
            return []
