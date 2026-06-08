<img align="left" height="100" style="margin-right: 10px;" src="../img/icon.png">

# IDkollen Python Client

[![PyPI][pypi-image]][pypi-url]
[![Downloads][downloads-image]][downloads-url]
[![Documentation][docs-image]][docs-url]
[![MIT license][license-image]][license-url]

[pypi-image]: https://img.shields.io/pypi/v/idkollen-client?style=flat-square
[pypi-url]: https://pypi.org/project/idkollen-client/
[downloads-image]: https://img.shields.io/pypi/dm/idkollen-client?style=flat-square
[downloads-url]: https://pypi.org/project/idkollen-client/
[docs-image]: https://img.shields.io/badge/github-docs-orange?logo=github&style=flat-square
[docs-url]: https://idkollen.github.io/idk-clients/py
[license-image]: https://img.shields.io/badge/license-MIT-blue?style=flat-square
[license-url]: https://opensource.org/license/mit

API client for the [IDkollen](https://developers.idkollen.se) REST API. Supports both synchronous and async usage via [httpx](https://www.python-httpx.org/) and [Pydantic](https://docs.pydantic.dev/) models.

## Installation

```sh
pip install idkollen-client
```

## Usage

### Synchronous

```python
from idkollen_client import IdkollenClientBuilder, BankIdSeAuthRequest, PollOptions

client = IdkollenClientBuilder("client_id", "client_secret") \
    .environment("staging") \
    .build()

session = client.bankid_se().auth(BankIdSeAuthRequest())
result = client.bankid_se().wait_for_auth(session.id, PollOptions())

print(result)
```

### Async

```python
import asyncio
from idkollen_client import IdkollenClientBuilder, BankIdSeAuthRequest, PollOptions

async def main():
    client = IdkollenClientBuilder("client_id", "client_secret") \
        .environment("staging") \
        .build_async()

    session = await client.bankid_se().auth(BankIdSeAuthRequest())
    result = await client.bankid_se().wait_for_auth(session.id, PollOptions())

    print(result)

asyncio.run(main())
```

## Development

#### Prerequisites

* [Python 3.10+](https://www.python.org/)
* [uv](https://docs.astral.sh/uv/)

#### Install dependencies

```sh
uv sync --extra dev
```
