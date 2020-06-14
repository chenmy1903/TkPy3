# -*- encoding: UTF-8 -*-
import os
from fastapi import FastAPI
import uvicorn
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from TkPy3.version import version as tkpy_version
from TkPy3.locale_dirs import BASE_DIR, images_icon_dir
from starlette.requests import Request

app = FastAPI(title='TkPy3文档', version=tkpy_version, description='TkPy3 使用PyQt5做的TkPy IDE')
app.mount('/static', StaticFiles(directory=os.path.join(BASE_DIR, 'tkpy_doc', 'static')), name='static')
app.mount('/images_icon', StaticFiles(directory=images_icon_dir),
          name='images_icon')
templates = Jinja2Templates(os.path.join(BASE_DIR, 'tkpy_doc', "templates"))

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

def main():
    uvicorn.run(app, port=8084)

if __name__ == "__main__":
    main()
