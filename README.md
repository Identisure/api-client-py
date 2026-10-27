<img align="left" height="100" style="margin-right: 10px;" src="img/icon.png">

# Identisure Python Client

[![PyPI][pypi-image]][pypi-url]
[![Downloads][downloads-image]][downloads-url]
[![Documentation][docs-image]][docs-url]
[![MIT license][license-image]][license-url]

[pypi-image]: https://img.shields.io/pypi/v/identisure-client?style=flat-square
[pypi-url]: https://pypi.org/project/identisure-client/
[downloads-image]: https://img.shields.io/pypi/dm/identisure-client?style=flat-square
[downloads-url]: https://pypi.org/project/identisure-client/
[docs-image]: https://img.shields.io/badge/github-docs-orange?logo=github&style=flat-square
[docs-url]: https://identisure.github.io/api-client-py
[license-image]: https://img.shields.io/badge/license-MIT-blue?style=flat-square
[license-url]: https://opensource.org/license/mit

API client for the [Identisure](https://developers.identisure.com) REST API. Supports both synchronous and async usage via [httpx](https://www.python-httpx.org/) and [Pydantic](https://docs.pydantic.dev/) models.

## Requirements

Python 3.10 or later.

## Supported providers

- **BankID SE**: auth, sign, phone auth and sign, QR verify, age verification
- **BankID NO**: auth, backchannel auth, sign, age verification
- **Freja eID**: auth, backchannel auth, sign, backchannel sign, age verification
- **MitID**: auth, backchannel auth, sign, age verification
- **FTN** (Finnish Trust Network): auth, age verification
- **Vipps MobilePay**: auth, backchannel auth
- **Documents**: upload and download documents for signing

## Installation

```sh
pip install identisure-client
```

## Usage

### Synchronous

```python
from identisure_client import IdentisureClientBuilder, BankIdSeAuthRequest, PollOptions

with IdentisureClientBuilder("client_id", "client_secret").environment("staging").build() as client:
    session = client.bankid_se().auth(BankIdSeAuthRequest())
    result = client.bankid_se().wait_for_auth(session.id, PollOptions())

print(result)
```

### Async

```python
import asyncio
from identisure_client import IdentisureClientBuilder, BankIdSeAuthRequest, PollOptions


async def main():
    async with (
        IdentisureClientBuilder("client_id", "client_secret")
        .environment("staging")
        .build_async() as client
    ):
        session = await client.bankid_se().auth(BankIdSeAuthRequest())
        result = await client.bankid_se().wait_for_auth(session.id, PollOptions())

    print(result)


asyncio.run(main())
```

### Verifying callbacks

Pass the raw request body exactly as received, before parsing it.

```python
from identisure_client import verify_callback_signature

valid = verify_callback_signature(raw_body, headers["X-Signature-SHA256"], hmac_secret)
```

## Development

#### Prerequisites

* [Python 3.10+](https://www.python.org/)
* [uv](https://docs.astral.sh/uv/)
* [just](https://just.systems/)

#### Clone

The test fixtures live in a git submodule, so clone with `--recurse-submodules` (or run `git submodule update --init` in an existing clone).

```sh
git clone --recurse-submodules https://github.com/identisure/api-client-py.git
```

#### Install dependencies

```sh
uv sync --extra dev
```

#### Build, test and lint

```sh
just build
just test
just check
```

## Other languages

[C#](https://github.com/identisure/api-client-csharp), [Dart](https://github.com/identisure/api-client-dart), [Go](https://github.com/identisure/api-client-go), [TypeScript/JavaScript](https://github.com/identisure/api-client-js), [Java/Kotlin](https://github.com/identisure/api-client-jvm), [PHP](https://github.com/identisure/api-client-php), [Ruby](https://github.com/identisure/api-client-ruby), [Rust](https://github.com/identisure/api-client-rust), [Swift](https://github.com/identisure/api-client-swift)
