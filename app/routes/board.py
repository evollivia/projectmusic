from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse , RedirectResponse
from starlette.templating import Jinja2Templates

from app.dbfactory import get_db
from app.schema.board import BoardCreate
from app.service.board import BoardService, get_board_data, process_upload, FileService

board_router= APIRouter()
templates = Jinja2Templates(directory='views/templates')

@board_router.get('/list/{cpg}', response_class=HTMLResponse)
async def list(req: Request, cpg: int, db: Session = Depends(get_db)):
    try:
        stpgb = int((cpg - 1) / 10) * 10 + 1
        bdlist = BoardService.select_board(db, cpg)
        return templates.TemplateResponse('/board/list.html',
                                          {'request': req, 'bdlist': bdlist, 'cpg': cpg, 'stpgb':stpgb})

    except Exception as ex:
        print(f'▷▷▷ list 오류 발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)

@board_router.get('/write', response_class=HTMLResponse)
async def write(req: Request):
    return templates.TemplateResponse('/board/write.html',{'request': req})

@board_router.post('/write')
async def writeok(req: Request, board: BoardCreate = Depends(get_board_data),
                  files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    try:
        print(board)
        attachs = await process_upload(files)
        print(attachs)
        if FileService.insert_board(board, attachs, db):
            return RedirectResponse('/board/list/1',303)

    except Exception as ex:
        print(f'▷▷▷writeok 오류발생 {str(ex)}')
        return RedirectResponse('/member/error',303)

@board_router.get('/view')
async def view(req: Request):
    return templates.TemplateResponse('board/view.html', {'request': req})

@board_router.get('/modify')
async def modify(req: Request):
    return templates.TemplateResponse('board/modify.html', {'request': req})




