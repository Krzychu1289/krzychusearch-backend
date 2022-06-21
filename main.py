import os
from dotenv import load_dotenv

import asyncio
import motor.motor_asyncio
import aiohttp.web

from routes.route_search import SearchRoute

load_dotenv()

mongodb_uri = os.environ.get("MONGODB_URI")

import asyncio
import motor.motor_asyncio
import aiohttp.web

routes = aiohttp.web.RouteTableDef()

if __name__ == "__main__":
    app = aiohttp.web.Application()
    app['db'] = motor.motor_asyncio.AsyncIOMotorClient(mongodb_uri)['krzychusearch']
    app['db'].get_io_loop = asyncio.get_running_loop
    app.add_routes(routes)
    SearchRoute(app)
    aiohttp.web.run_app(app, port=8888)

