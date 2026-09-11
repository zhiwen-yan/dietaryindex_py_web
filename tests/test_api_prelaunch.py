from types import SimpleNamespace

from fastapi.testclient import TestClient

import dietaryindex_api.app as api_module


def test_healthz_is_public():
    client = TestClient(api_module.app)
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["x-request-id"]


def test_request_id_is_preserved():
    client = TestClient(api_module.app)
    response = client.get("/healthz", headers={"x-request-id": "client-trace-123"})
    assert response.headers["x-request-id"] == "client-trace-123"


def test_v1_routes_require_api_key_when_enabled(monkeypatch):
    monkeypatch.setattr(
        api_module,
        "settings",
        SimpleNamespace(
            runtime_dir="runtime_data",
            api_key="secret123",
            require_api_key=True,
        ),
    )
    client = TestClient(api_module.app)

    blocked = client.get("/v1/indices")
    assert blocked.status_code == 401

    allowed = client.get("/v1/indices", headers={"x-api-key": "secret123"})
    assert allowed.status_code == 200


def test_upload_rejects_unsupported_file_type():
    client = TestClient(api_module.app)
    response = client.post(
        "/v1/uploads",
        files={"file": ("payload.exe", b"not-an-executable", "application/octet-stream")},
    )
    assert response.status_code == 415


def test_upload_response_does_not_expose_local_path():
    client = TestClient(api_module.app)
    response = client.post(
        "/v1/uploads",
        files={"file": ("../safe.csv", b"id,value\n1,2\n", "text/csv")},
    )
    assert response.status_code == 200
    assert response.json()["filename"] == "safe.csv"
    assert "path" not in response.json()


def test_upload_preview_serializes_missing_values_as_null():
    client = TestClient(api_module.app)
    response = client.post(
        "/v1/uploads",
        files={"file": ("missing.csv", b"id,value\n1,\n2,3\n", "text/csv")},
    )
    assert response.status_code == 200
    assert response.json()["preview"]["preview"][0]["value"] is None


def test_fisi_catalog_exposes_real_nhanes_adapters():
    client = TestClient(api_module.app)
    response = client.get("/v1/indices/FISI")
    assert response.status_code == 200
    payload = response.json()
    assert {"nhanes_fped", "nhanes_mped"}.issubset(payload["supported_modes"])
    for mode in ("nhanes_fped", "nhanes_mped"):
        requirement = payload["mode_requirements"][mode]
        assert requirement["required_file_keys"] == ["nutrient_path"]
        assert requirement["visible_file_keys"] == [
            "nutrient_path",
            "nutrient_ind_path",
            "nutrient_path2",
            "nutrient_ind_path2",
            "demo_path",
        ]


def test_nutrient_indices_expose_supported_source_modes():
    client = TestClient(api_module.app)
    expected = {"general", "asa24", "dhq3", "block"}
    for index_key in ("FISI", "NRF", "NAR", "MAR", "INQ", "PRAL", "NEAP", "CDAI"):
        response = client.get(f"/v1/indices/{index_key}")
        assert response.status_code == 200
        assert expected.issubset(response.json()["supported_modes"])


def test_fii_database_is_available():
    client = TestClient(api_module.app)
    summary = client.get("/v1/fii/summary")
    assert summary.status_code == 200
    assert summary.json()["foods"] > 9_000
    assert summary.json()["groups"] > 10

    search = client.get("/v1/fii/search", params={"q": "apple", "limit": 3})
    assert search.status_code == 200
    items = search.json()["items"]
    assert 0 < len(items) <= 3
    assert all("apple" in item["food"].lower() for item in items)

    fdcd = items[0]["fdcd"]
    by_code = client.get("/v1/fii/search", params={"q": str(fdcd), "limit": 3})
    assert by_code.status_code == 200
    assert [item["fdcd"] for item in by_code.json()["items"]] == [fdcd]

    unsupported_chinese = client.get("/v1/fii/search", params={"q": "苹果"})
    assert unsupported_chinese.status_code == 200
    assert unsupported_chinese.json()["items"] == []

    filtered = client.get(
        "/v1/fii/search",
        params={"q": "", "direction": "pro", "sort_by": "fii_desc", "limit": 5},
    )
    assert filtered.status_code == 200
    assert len(filtered.json()["items"]) == 5
    assert all(item["direction"] == "pro" for item in filtered.json()["items"])

    peers = client.get(f"/v1/fii/foods/{fdcd}/peers")
    assert peers.status_code == 200
    assert peers.json()["food_group"] == items[0]["food_group"]
