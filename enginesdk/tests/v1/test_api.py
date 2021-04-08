import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from enginesdk.api import EngineAPI
from enginesdk.tests.v1.factories import PredictFactory
from enginesdk.config import get_settings

settings = get_settings()


@pytest.fixture
def test_predictor():
    return PredictFactory().mock_predictor()


class TestEngineAPI:
    @pytest.fixture
    def client(self, test_predictor):
        api = EngineAPI(test_predictor).api

        return TestClient(api)

    def test_get_healthcheck(self, client):
        response = client.get("/healthcheck")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Service online"
        assert data["version"] == settings.REVISION
        assert "time" in data

    def test_get_schema(self, client, test_predictor):
        response = client.get("/v1/schema")
        assert response.status_code == 200
        assert response.json() == {
            "input": test_predictor.Input.schema(),
            "output": test_predictor.Output.schema(),
        }

    def test_get_info(self, client, test_predictor):
        response = client.get("/v1/info")
        assert response.status_code == 200
        data = response.json()
        assert data["schema"] == {
            "input": test_predictor.Input.schema(),
            "output": test_predictor.Output.schema(),
        }
        assert "settings" in data

    def test_post_predict(self, client, test_predictor):
        response = client.post(
            "/v1/predict", json=test_predictor.factory.mock_input().dict()
        )
        assert response.status_code == 200
        for key in test_predictor.Output.__fields__:
            assert key in response.json()

    def test_post_predict_with_gid(self, client, test_predictor):
        response = client.post(
            "/v1/predict/test",
            json=test_predictor.factory.mock_input().dict(),
        )
        assert response.status_code == 200
