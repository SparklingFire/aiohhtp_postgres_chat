from main_page.routes import routes as main_page_routers


def routes_aggregator():
    routes = []
    routes.extend(main_page_routers)
    return routes
