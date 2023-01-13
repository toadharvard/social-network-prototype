from fastapi.testclient import TestClient
from fastapi import status


class TestPingRouter:
    @property
    def default_api_url(self):
        return "api/ping"

    def test_ping(self, client: TestClient):
        resp = client.get(self.default_api_url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json() == "Pong!"
