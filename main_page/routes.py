from .handlers import MainPage, NewsList, NewsDetails


routes = [('GET', '/main/', MainPage, 'main_page'),
          ('GET', '/main/news/', NewsList, 'news-list'),
          ('GET', '/main/news/{news_id}/', NewsDetails, 'news-details')
          ]
