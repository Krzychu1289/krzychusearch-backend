import typing


class SearchResult:
    
    def __init__(self, document: typing.Dict[str, typing.Union[None, str]]):
        self._title: typing.Union[None, str] = document["title"]
        self._link: typing.Union[None, str] = document["link"]
        self._description: typing.Union[None, str] = document["description"]
        self._author: typing.Union[None, str] = document["author"]
        self._views: typing.Union[None, str] = document["views"]
        self._image: typing.Union[None, str] = document["image"]
        self._tags: typing.Union[None, typing.List[str]] = document["tags"]
    
    def all(self) -> typing.Dict[str, typing.Union[None, str]]:
        return {
            "title": self._title,
            "link": self._link,
            "description": self._description,
            "author": self._author,
            "views": self._views,
            "image": self._image,
            "tags": self._tags
        }
    
    async def check(self):
        none_values = []
        if self._title is None:
            none_values.append("title")
        if self._link is None:
            none_values.append("link")
        if self._description is None:
            none_values.append("description")
        if self._author is None:
            none_values.append("author")
        if self._views is None:
            none_values.append("views")
        
        if len(none_values) > 0:
            return "Please fill up these following values in your json: " + ", "\
                .join(none_value for none_value in none_values)
        
        else:
            return None
    
    @property
    def title(self) -> typing.Union[None, str]:
        return self._title
    
    @property
    def link(self) -> typing.Union[None, str]:
        return self._link
        
    @property
    def description(self) -> typing.Union[None, str]:
        return self._description
    
    @property
    def author(self) -> typing.Union[None, str]:
        return self._author
    
    @property
    def views(self) -> typing.Union[None, str]:
        return self._views
        