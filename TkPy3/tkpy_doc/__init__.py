# -*- encoding: UTF-8 -*-
import importlib
import os
from fastapi import FastAPI
import uvicorn
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from TkPy3.tkpy_doc.serever_configs import port
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


@app.get('/python/package/help/get/')
@app.get('/python/package/help/get/{package_name}')
def get_python_package_help(request: Request, package_name: str = None):
    if not package_name:
        return templates.TemplateResponse('show_text.html',
                                          {'request': request, 'text': '请在上方输入包名', 'title': '请在上方输入包名'})
    try:
        module = importlib.import_module(package_name)
        try:
            module_file = module.__file__
            if not module.__file__:
                raise AttributeError()
        except AttributeError:
            module_file = '这个包没有文件'
        if not module.__doc__:
            module.__doc__ = '没有文档'
        text = f'包文件: {module_file}\n{module.__doc__}'
        return templates.TemplateResponse('show_text.html',
                                          {'request': request, 'text': text, 'title': f'{package_name} 的文档'})
    except ImportError:
        return templates.TemplateResponse('show_text.html',
                                          {'request': request, 'text': '未安装此包。',
                                           'title': f'未找到此包 (Package name = {package_name})'})


@app.get('/python/package/help')
def python_package_help(request: Request):
    return templates.TemplateResponse('package_help.html', {'request': request})


def main(*, port: int = port):
    return uvicorn.run(app, port=port)


run_server = main

if __name__ == "__main__":
    print(main())
