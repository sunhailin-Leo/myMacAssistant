import os
import json
from typing import List

from app.utils import synchronized


class ChromeBookmarksParser:
    _instance = None

    def __init__(self):
        self._path: str = "~/Library/Application Support/Google/Chrome/Default/Bookmarks"
        p = self._get_current_user_root_path()
        self._path = self._path.replace("~", p)

        self._data: List = []

    @synchronized
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def _get_current_user_root_path() -> str:
        return "/{}".format("/".join(os.getcwd().split("/")[1:3]))

    def _flatten_data(self, data: List):
        for d in data:
            if d.get("children") is None:
                # print(f"当前解析的书签标题: {d['name']}, 对应的 URL: {d['url']}")
                self._data.append({"name": d["name"], "url": d["url"]})
            else:
                self._flatten_data(data=d.get("children"))

    def load_bookmarks(self):
        bookmarks_json = json.load(open(self._path, "r"))
        for k, v in bookmarks_json["roots"].items():
            if k == "synced":
                continue
            if isinstance(v, dict) is not True:
                continue
            if v.get("children") is not None:
                self._flatten_data(data=v.pop("children"))
                # print(f"当前书签栏的名字: {v['name']}")
        return self

    def get_data(self):
        return self._data
