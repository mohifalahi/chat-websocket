import asyncio

import aiohttp
import pytest
from websockets.asyncio.client import connect

pytest_plugins = ("pytest_asyncio",)


async def send_api_call(count: int):
    await asyncio.sleep(1)
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8000/user/broadcast"
        async with session.post(url, data={"message": "hi clients"}) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data["message"] == "message broadcast successfully"
            assert data["receiver_count"] == count


async def connnect_websocket_client():
    uri = "ws://localhost:8000/ws/subscribe"
    async with connect(uri) as websocket:
        greeting = await websocket.recv()


@pytest.mark.asyncio
async def test_no_websocket_clients():
    await asyncio.gather(send_api_call(0))


@pytest.mark.asyncio
async def test_some_websocket_clients():
    await asyncio.gather(
        connnect_websocket_client(),
        connnect_websocket_client(),
        connnect_websocket_client(),
        send_api_call(3),
    )
