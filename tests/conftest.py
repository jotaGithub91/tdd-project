import pytest
import pytest_asyncio
import asyncio
from uuid import UUID
from store.db.mongo import db_client
from store.schemas.product import ProductIn, ProductUpdate
from store.usecases.product import product_usecase
from tests.factories import product_data, products_data
from httpx import AsyncClient

# @pytest_asyncio.fixture(scope="session")
@pytest.mark.asyncio(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mongo_client():
    return db_client.get()

@pytest_asyncio.fixture(autouse=True)
async def clear_collections(mongo_client):
    yield
    collections_names = await mongo_client.get_database().list_collection_names()
    for collection_name in collections_names:
        if collection_name.startswith("system"):
            continue

        await mongo_client.get_database()[collection_name].delete_many({})

@pytest_asyncio.fixture
async def client() -> AsyncClient:
    from store.main import app

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def products_url() -> str:
    return "/products/"

@pytest.fixture
def product_id() -> UUID:
    return UUID("fce6cc37-10b9-4a8e-a8b2-977df327001a")

@pytest.fixture
def product_in(product_id):
    return ProductIn(**product_data(), id=product_id)

@pytest.fixture
def product_up(product_id):
    return ProductUpdate(**product_data(), id=product_id)

@pytest_asyncio.fixture
async def product_inserted(product_in):
    return await product_usecase.create(body=product_in)

@pytest_asyncio.fixture
def products_in():
    return [ProductIn(**product) for product in products_data()]

@pytest_asyncio.fixture
async def products_inserted(products_in):
    return [await product_usecase.create(body=product_in) for product_in in products_in]