# Introduction

If you've ever tried to make an API wrapper
you probably know that the code written can
only be used as sync or async, well, not anymore.

## Features

- **Lightweight**: Extremely lightweight and minimal
- **Easy to use**: Implement features in no time with the
- **Async and blocking**: Provides both async and blocking calls
- **Test without a server**: Since the library internally uses httpx, it can be used to test itself using an `ASGI` or `WSGI` application.
- **DRY**: _Don't repeat yourself_, helps avoid code duplication and write reusable code
- **Routing**: An `APIRouter` class with simliar API to `APIClient`
- **Modular**: Create reusable routers that can be added to any client, independant of each other

## Example Usage

```py

from apiclient import APIClient, endpoint, Post

class CodeExecClient(APIClient):
  base_url = "https://pathtomysite.com/api/1.0"   # Note the missing / suffix
  @endpoint
  def run(self, language:str, code:str):
    # Do any processing with the data here!
    # Also note the / prefix in the url
    return Post("/execute", params={'lang':language, 'code':code})

```

## Documentation is under works
