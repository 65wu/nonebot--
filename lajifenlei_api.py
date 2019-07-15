import aiohttp
from aiocqhttp.message import escape


async def get_the_sort_of_trash(trash: str) -> str:
    sort = None
    url = f'https://laji.lr3800.com/api.php?name={trash}'
    async with aiohttp.request('GET', url) as resp:
        response = await resp.json(content_type='text/html')
        for news in response['newslist']:
            sort = news['type']

    print(response)
    if sort:
        trash_sort = {0: '可回收垃圾', 1: '有害垃圾', 2: '厨余垃圾', 3: '其他垃圾'}
        classification = trash_sort[sort]
        return f'{trash}属于{classification}'
    return '失败'
