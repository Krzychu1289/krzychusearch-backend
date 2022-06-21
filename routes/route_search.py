import difflib

import aiohttp
from aiohttp import web

from core.search_indexer import SearchIndex
from models.search_result import SearchResult

import validators


class SearchRoute:
    def __init__(self, app):
        self.app: aiohttp.web.Application = app
        self.app.add_routes([
            web.post("/engine/search", self.add_result),
            web.get("/engine/search", self.get_results),
            web.put("/engine/search", self.add_view_to_result)
        ])
    
    async def add_result(self, request: web.Request):
        data = await request.json()
        model = SearchResult(data)
        check = await model.check()
        if check is None:
            url_valid = validators.url(data["link"])
            if url_valid is True:
                db_data = await self.app['db'].search_results.find_one({"link": data["link"]})
                if db_data is None:
                    await self.app['db'].search_results.insert_one(data)
                    return web.json_response({"code": "200", "message": "Successfully added result"}, status=200)
                else:
                    return web.json_response({"code": "409", "message": "Result already exists"}, status=409)
            else:
                return web.json_response({"code": "400", "message": "Invalid URL"}, status=400)
        else:
            return web.json_response({"code": "406", "message": check}, status=406)
    
    async def get_results(self, request: web.Request):
        data = request.headers
        if data.get("query") is None:
            return web.json_response({"code": "400", "message": "Please provide a query"}, status=400)
        
        db_all = self.app['db']["search_results"].find({})
        
        indexer = SearchIndex(data.get("query"), db_all)
        
        results = await indexer.get_all_matching_results()
        print(results)

        if len(results) > 0:
            return web.json_response(results, status=200)
        else:
            return web.json_response([], status=200)
    
    async def add_view_to_result(self, request: web.Request):
        data = await request.json()
        if data["route"] is None:
            return web.json_response({"code": "400", "message": "Please provide a valid route"}, status=400)
        
        found_db = await self.app['db'].search_results.find_one({"link": data["route"]})
        if found_db is None:
            return web.json_response({"code": "400", "message": "Please provide a valid route"}, status=400)
        
        await self.app['db'].search_results.update_one({"link": data["route"]},
                                                 {"$set": {"views": str(int(found_db["views"]) + 1)}})
        return web.json_response({"code": "200", "message": "Successfully added view"}, status=200)
