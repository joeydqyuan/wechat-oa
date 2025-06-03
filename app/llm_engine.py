from openai import AsyncOpenAI
from app.config import settings

client = AsyncOpenAI(api_key=settings.llm_api_key, base_url=settings.llm_base_url)


async def gen_exercise_content():
    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {
                'role': 'system',
                'content': '你是一位专业的健身教练和营养师，擅长撰写关于身材管理的公众号文章',
            },
            {
                'role': 'user',
                'content': '请撰写一篇关于夏季身材管理的公众号文章，包含以下内容：\n1. 夏季饮食建议\n2. 适合夏季的室内外运动\n3. 常见误区解析\n4. 互动问答环节\n\n要求: 语言轻松活泼, 适合20-35岁女性读者, 500字左右',
            },
        ],
        stream=False,
        temperature=0.7,
    )
    content = response.choices[0].message.content
    return content
