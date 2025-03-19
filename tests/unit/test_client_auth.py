import pytest
import asyncio
import socketio
from uvicorn import Config, Server
from fastapi.testclient import TestClient

test_jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidGVzdF91c2VyIn0.LTzzf2Tajb2dhstlrw_wen660izMyzHFnxnhkbz2bRs'

@pytest.fixture
def set_app(monkeypatch):
    monkeypatch.setenv('CLIENT_AUTH', 'true')
    monkeypatch.setenv('JWT_SECRET_CLIENT_AUTH', 'secret-key-for-agent-auth')
    # import here to load env
    from openhands.server.listen import app
    return app


@pytest.fixture
def test_client(set_app):
    headers = {'Authorization':f'Bearer {test_jwt}', 'Content-Type':'application/json'}
    return TestClient(
        set_app,
        headers=headers
    )


def test_socket_connect(set_app, test_client):

    def start_socket_server(set_app):
        config = Config(set_app, host='127.0.0.1', port=3000)
        server = Server(config=config)
        config.setup_event_loop()
        loop = asyncio.get_event_loop()
        server_task = server.serve()
        asyncio.ensure_future(server_task)
        return server_task

    async def run_socket_client():
        response = test_client.post('/api/conversations', json={})
        assert response.status_code == 200
        conversation_id = response.json()['conversation_id']
        sio = socketio.AsyncClient()
        await sio.connect(
            f'http://localhost:3000?conversation_id={conversation_id}',
            auth={'token': f'Bearer {test_jwt}'}
        )
        response = test_client.delete(f'/api/conversations/{conversation_id}')
        assert response.status_code == 200


    start_socket_server(set_app)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_socket_client())

