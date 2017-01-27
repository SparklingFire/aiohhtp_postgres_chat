import json
import datetime
from time import strftime


async def jsoner(col_list, val_list):
    result = []
    for i in range(len(val_list)):
        article = {}
        for j in range(len(val_list[i])):
            value = val_list[i][j]
            if isinstance(value, datetime.date):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            article.update({col_list[j]: value})
        result.append(article)
    return json.dumps(result)


async def news_list_jsoned(request):
    database = request.app['db']
    async with database.acquire() as conn:
        columns_list = [x[0] for x in await
        conn.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='article'")
                        ]

        article_list = [x for x in await conn.execute('select * from article order by created')]
    return await jsoner(columns_list, article_list)
