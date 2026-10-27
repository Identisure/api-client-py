build:
    uv build

test:
    uv run --extra dev pytest

check:
    uv run --locked --extra dev ruff format --check .
    uv run --locked --extra dev ruff check .
    uv run --locked --extra dev mypy

publish:
    uv build
    uv publish

gen-doc:
    uv run --extra dev python -m pdoc -o docs identisure_client
