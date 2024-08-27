from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request

from app.dbfactory import get_db
from app.service.music import MusicService

music_router= APIRouter()

templates = Jinja2Templates(directory='views/templates')


@music_router.get('/index')
async def index(req: Request, db: Session = Depends(get_db)):
    try:
        mlist = MusicService.select_music(db)
        return templates.TemplateResponse('/music/index.html', {'request': req, 'mlist': mlist})
    except Exception as ex:
        print(f'▷▷▷ music_list 오류발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)


@music_router.get('/music')
async def music(req: Request):
    return templates.TemplateResponse('music/music.html', {'request': req})

@music_router.get('/musicvideo')
async def musicvideo(req: Request):
    return templates.TemplateResponse('music/musicvideo.html', {'request': req})

@music_router.get('/storage')
async def storage(req: Request):
    return templates.TemplateResponse('music/storage.html', {'request': req})

@music_router.get('/test')
async def test(req: Request):
    return templates.TemplateResponse('music/test.html', {'request': req})