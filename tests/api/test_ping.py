from fastapi.testclient import TestClient


class TestPingRouter:
    @property
    def default_api_url(self):
        return "api/ping"

    def test_ping(self, client: TestClient):
        resp = client.get(self.default_api_url)
        assert resp.status_code == 200
        assert resp.json() == "Pong!"
