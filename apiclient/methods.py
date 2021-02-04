from dataclasses import dataclass, field
from typing import Any

from httpx._types import (CookieTypes, FileTypes, HeaderTypes, QueryParamTypes,
                          RequestData, RequestFiles)

from .core import APIRouter

__all__ = ('Get', 'Post', 'Put', 'Patch', 'Delete', 'Request')


@dataclass
class Request:
    url: str
    method: str
    headers: HeaderTypes = field(default_factory=dict)
    params: QueryParamTypes = field(default_factory=dict)
    data: RequestData = field(default_factory=dict)
    json: Any = field(default_factory=dict)
    files: RequestFiles = field(default_factory=dict)
    cookies: CookieTypes = field(default_factory=dict)

    absolute_url: bool = False
    from_base_url: bool = False

    def dict(self, *, router: APIRouter):
        req_dict = {k: getattr(self, k) for k in (
            'method', 'headers', 'params', 'data', 'json', 'files', 'cookies')}

        if self.absolute_url:
            url = self.url
        elif self.from_base_url:
            url = router.base_url + self.url
        else:
            url = router.base_url + getattr(router, 'path', '') + self.url
        req_dict['url'] = url

        return req_dict


def Get(
    url: str, *,
    headers: HeaderTypes = {},
    params: QueryParamTypes = {},
    data: RequestData = {},
    json: Any = {},
    files: RequestFiles = {},
    cookies: CookieTypes = {},
    absolute_url: bool = False,
    from_base_url: bool = False,
) -> Any:
    return Request(url=url, method="GET", headers=headers, params=params, data=data, json=json, files=files)


def Post(
    url: str, *,
    headers: HeaderTypes = {},
    params: QueryParamTypes = {},
    data: RequestData = {},
    json: Any = {},
    files: RequestFiles = {},
    cookies: CookieTypes = {},
    absolute_url: bool = False,
    from_base_url: bool = False,
) -> Any:
    return Request(url=url, method="POST", headers=headers, params=params, data=data, json=json, files=files)


def Patch(
    url: str, *,
    headers: HeaderTypes = {},
    params: QueryParamTypes = {},
    data: RequestData = {},
    json: Any = {},
    files: RequestFiles = {},
    cookies: CookieTypes = {},
    absolute_url: bool = False,
    from_base_url: bool = False,
) -> Any:
    return Request(url=url, method="PATCH", headers=headers, params=params, data=data, json=json, files=files)


def Put(
    url: str, *,
    headers: HeaderTypes = {},
    params: QueryParamTypes = {},
    data: RequestData = {},
    json: Any = {},
    files: RequestFiles = {},
    cookies: CookieTypes = {},
    absolute_url: bool = False,
    from_base_url: bool = False,
) -> Any:
    return Request(url=url, method="PUT", headers=headers, params=params, data=data, json=json, files=files)


def Delete(
    url: str, *,
    headers: HeaderTypes = {},
    params: QueryParamTypes = {},
    data: RequestData = {},
    json: Any = {},
    files: RequestFiles = {},
    cookies: CookieTypes = {},
    absolute_url: bool = False,
    from_base_url: bool = False,
) -> Any:
    return Request(url=url, method="DELETE", headers=headers, params=params, data=data, json=json, files=files)
