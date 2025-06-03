from typing import Union
from fastapi import FastAPI
from app.wechat_oa import publish_exercise_related_article


app = FastAPI()


@app.get('/')
async def read_root():
    return {'Hello': 'World'}


@app.post('/wechat-oa-publish-article')
async def wechat_oa_pulish_article():
    data = await publish_exercise_related_article()
    return {'data': data}
