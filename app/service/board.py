import os

from fastapi import Form, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError
from app.model.board import Board, BoardFile
from app.schema.board import BoardCreate

UPLOAD_PATH = 'D:/test/'

def get_board_data(title: str = Form(...), userid: str = Form(...),
                   contents: str = Form(...)):
    return BoardCreate(userid=userid, title=title, contents=contents)

async def process_upload(files):
    attachs = [] # 업로드된 파일정보를 저장하기 위해 리스트 생성
    from datetime import datetime
    today = datetime.today().strftime('%Y%m%d%H%M%S') # UUID 생성 (유니크한 고유 식별값 생성)
    for file in files:
        if file.filename != '' and file.size > 0:
            nfname = f'{today}{file.filename}'
            # os.path.join(A,B) => A/B (경로생성)
            fname = os.path.join(UPLOAD_PATH, nfname) # 업로드할 파일경로 생성
            content = await file.read()  # 업로드할 파일의 내용을 비동기로 읽음
            with open(fname, 'wb') as f:
                f.write(content)
            attach = [nfname, file.size] # 업로드된 파일 정보를 리스트에 저장
            attachs.append(attach)

    return attachs

class FileService:
    @staticmethod
    def insert_board(fl, attachs, db):
        try:
            with db.begin():
                stmt = insert(Board).values(userid=fl.userid,
                                            title=fl.title, contents=fl.contents)
                result = db.execute(stmt)

                # 방금 생성한 레코드의 기본키 값 : inserted_primary_key
                inserted_bno = result.inserted_primary_key[0]

                for attach in attachs:
                    data = {'fname': attach[0], 'fsize': attach[1],
                            'bno': inserted_bno}
                    stmt = insert(BoardFile).values(data)
                    result = db.execute(stmt)

                db.commit()

                return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ insert_gallery에서 오류발생 : {str(ex)}')
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to insert board data")

class BoardService:
    @staticmethod
    def select_board(db, cpg):
            try:
                stbno = (cpg - 1 ) * 25
                stmt = select(Board.bno, Board.title, Board.userid, Board.regdate, Board.views) \
                    .order_by(Board.bno.desc()) \
                    .offset(stbno).limit(25)
                result = db.execute(stmt)
                return result

            except SQLAlchemyError as ex:
                print(f'▶▶▶ select_board 오류발생 : {str(ex)}')