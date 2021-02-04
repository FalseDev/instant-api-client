import inspect
from typing import (Any, Awaitable, Callable, Dict, List, Mapping, Optional,
                    Tuple, TypeVar, Union)

from httpx._client import BaseClient

__all__ = ('APIRouter', 'APIClient', 'endpoint')

_F = TypeVar("_F")


class BaseRouter:
    """Base class implementing 'route mounting' functionality"""
    def _initialize(self, **kwargs):
        """Looks for routers and routes and mount them

        Also handles calling the _pre_init and _post_init hooks
        """
        self._pre_init()
        self_is_router = isinstance(self, APIRouter)
        client = self.client if self_is_router else self
        for attr_name, attr_type in getattr(self, '__annotations__', {}).items():
            if issubclass(attr_type, APIRouter):
                setattr(self, attr_name, attr_type(client))

        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Endpoint):
                attr.register(router=self)
        self._post_init(**kwargs)

    def _pre_init(self):
        pass

    def _post_init(self, **kwargs):
        if kwargs:
            raise RuntimeError("Unexpected argument {} passed!".format(next(iter(kwargs.keys()))))


class APIClient(BaseRouter):

    # Declare these in the _post_init or as subclass attribute
    base_url: str

    def __init__(self, *, session: Union[BaseClient, Callable]):
        if callable(session):
            self.session = session()
        self.session = session
        self._post_processors = []
        self._initialize()


class APIRouter(BaseRouter):
    # Declare as subclass attribute
    path: str

    def __init__(self, client: APIClient):
        self.client = client
        self.session = client.session
        self.base_url = client.base_url
        self._post_processors = []
        self._initialize()


class Endpoint:
    def __init__(self, func):
        self.callback = func
        self.__doc__ = func.__doc__

        self.router = None
        self.session = None
        self.post_processors = []

    def register(self, *, router: APIRouter):
        self.router = router
        self.session = router.session
        # inherit all previous post processors
        self.post_processors.extend(router._post_processors)

        # post processor for this particular route
        post_processor_name = '_post_' + self.callback.__name__
        # add if avalable
        if hasattr(router, post_processor_name):
            self.post_processors.append(getattr(router, post_processor_name))

    def __call__(self, *args, **kwargs):
        request = self.callback(self.router, *args, **kwargs)

        httpx_request = self.session.build_request(**request.dict(router=self.router))

        if inspect.iscoroutinefunction(self.session.send):
            return self.async_call(httpx_request)
        return self.sync_call(httpx_request)

    def sync_call(self, httpx_request):
        response = self.session.send(httpx_request)
        print(self.post_processors, response)
        for post_processor in self.post_processors:
            response = post_processor(response)
            print(response)
        return response

    async def async_call(self, httpx_request):
        response = await self.session.send(httpx_request)
        for post_processor in self.post_processors:
            if inspect.iscoroutinefunction(post_processor):
                response = await post_processor(response)
            else:
                response = post_processor(response)
        return response


def endpoint(func: _F) -> _F:
    return Endpoint(func)
