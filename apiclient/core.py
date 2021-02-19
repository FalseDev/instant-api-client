import inspect
import os
from typing import (Any, Awaitable, Callable, Dict, List, Mapping, Optional,
                    Tuple, TypeVar, Union)

from httpx._client import BaseClient

__all__ = ('APIRouter', 'APIClient', 'endpoint')

_F = TypeVar("_F")

DOCS_MODE = os.environ.get("DOCS_MODE", False)

class Layer:
    def __init__(self, func):
        self.sync_func = func
        self.async_func = func

    def async_layer(self, func):
        self.async_func = func

class Endpoint:
    def __init__(self, func):
        self.__func__ = func
        self.parent:Optional[RouterBase] = None

    def copy(self):
        return self.__class__(self.__func__)

    def __call__(self, *args, **kwargs):
        request = self.__func__(self.parent, *args, **kwargs)
        httpx_request = self.session.build_request(request.dict(self.parent))
        layers = self.parent.layers + request.layers
        if inspect.iscoroutinefunction(self.session.send):
            return self.async_call(httpx_request, layers)
        return self.sync_call(httpx_request, layers)
    
    def sync_call(self, request, layers):
        res = self.session.send(request)
        for layer in layers:
            res = layer.sync_func(res)

    async def async_call(self, request, layers):
        res = self.session.send(request)
        for layer in layers:
            if inspect.iscoroutinefunction(layer.async_func):
                res = await layer.async_func(res)
            else:
                res = layer.async_func(res)

    @property
    def session(self):
        return self.parent.session

class RouterMeta(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        name = kwargs.pop('name', name)
        if kwargs.pop("no_init", False):
            return super().__new__(cls, name, bases, attrs, **kwargs)
        attrs['__routers__'] = {
            name: router
            for name, router in attrs.get('__annotations__', {}).items()
            if issubclass(router, APIRouter)
        }
        attrs['__endpoints__'] = {
            name: endpoint
            for name, endpoint in attrs.items()
            if isinstance(endpoint, Endpoint)
        }
        self = super().__new__(cls, name, bases, attrs, **kwargs)
        return self


class RouterBase(metaclass=RouterMeta, no_init=True):
    __endpoints__: Dict[str, str]
    __routers__: Dict[str, "APIRouter"]
    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)

        for name, endpoint in cls.__endpoints__.items():
            new_ep = endpoint.copy()
            new_ep.parent = self
            setattr(self, name, endpoint)

        for name, router in cls.__routers__.items():
            inst = router(self)
            # inst.parent = self
            setattr(self, name, inst)

        return self

class APIClient(RouterBase, no_init=True):
    base_url: str
    session: BaseClient

    @property
    def url(self):
        return self.base_url

    @property
    def layers(self) -> List[Union[Layer, Callable]]:
        return getattr(self, "__layers__", [])

class APIRouter(RouterBase, no_init=True):
    path: str
    def __init__(self, parent:RouterBase):
        self.parent = parent
        self.url = parent.url + self.path

    @property
    def session(self) -> BaseClient:
        return self.parent.session

    @property
    def layers(self) -> List[Union[Layer, Callable]]:
        return self.parent.layer + getattr(self, "__layers__", [])


def endpoint(func: _F) -> _F:  # Type check hack
    if DOCS_MODE:
        return func
    return Endpoint(func)
