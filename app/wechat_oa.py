import httpx
from app.config import settings
from app.llm_engine import gen_exercise_content


class WechatOfficialArticle:
    def __init__(self, title: str, content: str, digest: str):
        self.url_pre = settings.wc_cpi_bin_api
        self.title = title
        self.content = content
        self.digest = digest

    async def _get_token(self):
        token_url = f'{self.url_pre}/token?grant_type=client_credential&appid={settings.wc_app_id}&secret={settings.wc_app_secret}'
        async with httpx.AsyncClient() as client:
            resp = await client.get(token_url)
            data = resp.json()
            # need to check data
            # data = {
            #     'access_token': '92_qCwjyak6TXgdGOUXwwiF5xnJC-mln9DG12uEa2u7alJ_5CGeLwVcsttjmrcm_1qE3RcXxois86n003cRYLBXbEVsxaoExlXG5rogDNmuvGfzf4Jal8pXUpoOIecUTMiAJAGFY',
            #     'expires_in': 7200,
            # }
            self.access_token = data['access_token']

    async def _upload_cover_image(self):
        upload_url = f'{self.url_pre}/material/add_material?access_token={self.access_token}&type=image'
        cover_image_path = '/Users/yuandaoqing/Downloads/ai-image.jpeg'
        with open(cover_image_path, 'rb') as f:
            files = {'media': f}
            async with httpx.AsyncClient() as client:
                resp = await client.post(upload_url, files=files)
                data = resp.json()
                thumb_media_id = data['media_id']
                self.thumb_media_id = thumb_media_id
        # self.thumb_media_id = (
        #     'RZiq6AEQoiA0bmWtN9qxRmhnZm-0D1Eu3K0VIGJG_h8Q8LFSpdAh2ABw82Tb8-fW'
        # )

    async def _create_draft(self):
        draft_url = f'{self.url_pre}/draft/add?access_token={self.access_token}'
        payload = {
            'articles': [
                {
                    'article_type': 'news',
                    'thumb_media_id': self.thumb_media_id,
                    'title': self.title,
                    'content': self.content,
                    'digest': self.digest,
                }
            ]
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(draft_url, json=payload)
            data = resp.json()
            self.draft_media_id = data['media_id']

    async def _publish_draft(self):
        publish_url = (
            f'{self.url_pre}/freepublish/submit?access_token={self.access_token}'
        )
        payload = {'media_id': self.draft_media_id}

        async with httpx.AsyncClient() as client:
            resp = await client.post(publish_url, json=payload)
            data = resp.json()
            print(data)

    async def publish_to_wechat(self):
        await self._get_token()
        await self._upload_cover_image()
        await self._create_draft()
        await self._publish_draft()
        return 'done'


async def publish_exercise_related_article():
    content = await gen_exercise_content()
    title = '夏日身材保卫战'
    digest = '夏季身材管理全攻略，轻松拥有完美身材！'
    wc_oa = WechatOfficialArticle(title=title, content=content, digest=digest)
    return await wc_oa.publish_to_wechat()

