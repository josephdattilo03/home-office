from abc import ABC, abstractclassmethod, abstractmethod
from typing import ClassVar, TypeVar, Generic

import instaloader
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from urllib.parse import ParseResult, urlparse

#
# load_dotenv()
#
# username: str = os.environ["INSTAGRAM_USERNAME"]
# password: str = os.environ["INSTAGRAM_PASSWORD"]
#
#
# L = instaloader.Instaloader()
# L.login(username, password)
# L.load_session_from_file(username)


class FetcherResult(BaseModel):
    pass


class InstagramResult(FetcherResult):
    pass


class YoutubeResult(FetcherResult):
    pass


R = TypeVar("R", bound=FetcherResult)


class LinkFetcher(ABC, Generic[R]):
    hosts: ClassVar[frozenset[str]] = frozenset()
    _registry: ClassVar[list[type["LinkFetcher"]]] = []
    _instances: ClassVar[
        dict[type["LinkFetcher"], "LinkFetcher"]
    ]  # caching fetcher instances so we can save sessions

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if cls.hosts:
            LinkFetcher._registry.append(cls)

    @classmethod
    def can_handle(cls, url: str) -> bool:
        return urlparse(url).hostname in cls.hosts

    @classmethod
    def for_url(cls, url: str) -> "LinkFetcher[FetcherResult]":
        for fetcher_cls in cls._registry:
            if fetcher_cls.can_handle(url):
                if fetcher_cls not in cls._instances:
                    cls._instances[fetcher_cls]
                return cls._instances[fetcher_cls]
        raise ValueError(f"No parser for {url}")

    @abstractmethod
    def fetch(self, url: str) -> R: ...


class InstagramFetcher(LinkFetcher[InstagramResult]):
    hosts = frozenset(
        {"instagram.com", "ig.me", "cdninstagram.com", "instagr.am", "igsonar.com"}
    )
    pass


class YoutubeFetcher(LinkFetcher[YoutubeResult]):
    hosts = frozenset({"youtube.com", "m.youtube.com"})
    pass
