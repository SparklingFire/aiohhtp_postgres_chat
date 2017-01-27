from aiohttp import web
import aiohttp_jinja2
from main_page.utils import news_list_jsoned


class MainPage(web.View):
    async def get(self):
        return aiohttp_jinja2.render_template('main.html', self.request, context={})


class NewsList(web.View):
    async def get(self):
        return web.json_response(await news_list_jsoned(self.request))


class NewsDetails(web.View):
    async def get(self):
        pass
