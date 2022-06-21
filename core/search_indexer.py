import asyncio
import difflib
from typing import List, Union

from models.search_result import SearchResult


async def sequence_match(word: str, possibilities: List[dict], cutoff: Union[float, int], key: str) -> List[dict]:
    results = []
    for possibility in possibilities:
        if difflib.SequenceMatcher(None, str(word).lower(), possibility[key].lower()).ratio() >= cutoff:
            results.append(possibility)
    
    return results


class SearchIndex:
    def __init__(self, search_query, db_collection):
        self.search_query = search_query
        self.db_collection = db_collection
        
        self.final_results = []
    
    async def get_results_from_title(self, db_docs):
        first_results = await sequence_match(word=str(self.search_query), possibilities=db_docs, cutoff=0.7,
                                             key="title")
        
        if len(first_results) <= 1:
            second_results = await sequence_match(word=str(self.search_query), possibilities=db_docs, cutoff=0.6,
                                                  key="title")
            
            if len(second_results) <= 1:
                third_results = await sequence_match(word=str(self.search_query), possibilities=db_docs, cutoff=0.3,
                                                     key="title")
                for result in third_results:
                    if result not in self.final_results:
                        self.final_results.append(SearchResult(result).all())
            else:
                for result in second_results:
                    if result not in self.final_results:
                        self.final_results.append(SearchResult(result).all())
        else:
            for result in first_results:
                if result not in self.final_results:
                    self.final_results.append(SearchResult(result).all())
    
    async def get_results_from_url(self, db_docs):
        
        first_results = await sequence_match(word=str(self.search_query), possibilities=db_docs, cutoff=0.7, key="link")
        
        if len(first_results) <= 1:
            second_results = await sequence_match(word=str(self.search_query), possibilities=db_docs, cutoff=0.6,
                                                  key="link")
            
            if len(second_results) <= 1:
                third_results = await sequence_match(word=str(self.search_query), possibilities=db_docs, cutoff=0.3,
                                                     key="link")
                for result in third_results:
                    if result not in self.final_results:
                        self.final_results.append(SearchResult(result).all())
            else:
                for result in second_results:
                    if result not in self.final_results:
                        self.final_results.append(SearchResult(result).all())
        else:
            for result in first_results:
                if result not in self.final_results:
                    self.final_results.append(SearchResult(result).all())
    
    async def get_results_from_description(self, db_docs):
        
        first_results = await sequence_match(word=str(self.search_query), possibilities=db_docs, cutoff=0.7,
                                             key="description")
        
        if len(first_results) <= 1:
            second_results = await sequence_match(word=str(self.search_query), possibilities=db_docs, cutoff=0.6,
                                                  key="description")
            
            if len(second_results) <= 1:
                third_results = await sequence_match(word=str(self.search_query), possibilities=db_docs, cutoff=0.3,
                                                     key="description")
                for result in third_results:
                    if result not in self.final_results:
                        self.final_results.append(SearchResult(result).all())
            else:
                for result in second_results:
                    if result not in self.final_results:
                        self.final_results.append(SearchResult(result).all())
        else:
            for result in first_results:
                if result not in self.final_results:
                    self.final_results.append(SearchResult(result).all())
    
    async def get_results_from_tags(self, db_docs):
        for doc in db_docs:
            if self.search_query in doc["tags"]:
                if doc not in self.final_results:
                    self.final_results.append(SearchResult(doc).all())
    
    async def get_all_matching_results(self):
        db_docs = []
        async for doc in self.db_collection:
            db_docs.append(SearchResult(doc).all())
        
        processes = [self.get_results_from_tags(db_docs), self.get_results_from_title(db_docs),
                     self.get_results_from_url(db_docs), self.get_results_from_description(db_docs)]
        
        await asyncio.gather(*processes)
        
        return self.final_results
