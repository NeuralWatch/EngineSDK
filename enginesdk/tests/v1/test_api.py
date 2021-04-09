import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from enginesdk.tests.v1.factories import PredictFactory
from enginesdk import api, config


@pytest.fixture
def test_predictor():
    return PredictFactory().mock_predictor()


class TestEngineAPI:
    @pytest.fixture
    def engine_api(self, test_predictor):
        return api.EngineAPI(test_predictor).api

    @pytest.fixture
    def client(self, engine_api, test_predictor):
        return TestClient(engine_api)

    @pytest.fixture
    def settings(self):
        return config.get_settings()

    def test_get_healthcheck(self, client, settings):
        response = client.get("/healthcheck")
        assert response.status_code == 200

        data = response.json()
        assert data["message"] == "Service online"
        assert data["version"] == settings.REVISION
        assert "time" in data

    def test_get_schema(self, client, test_predictor):
        response = client.get("/v1/schema")
        assert response.status_code == 200

        data = response.json()
        assert data == {
            "input": test_predictor.Input.schema(),
            "output": test_predictor.Output.schema(),
        }

    def test_broadcast_online_status(self, client):
        response = client.get("/v1/broadcast")
        assert response.status_code == 200

    def test_get_info(self, client, test_predictor, settings):
        response = client.get("/v1/info")
        assert response.status_code == 200

        data = response.json()
        assert data["schema"] == {
            "input": test_predictor.Input.schema(),
            "output": test_predictor.Output.schema(),
        }
        assert "settings" in data
        assert data["settings"]["engine_slug"] == settings.ENGINE_SLUG

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
