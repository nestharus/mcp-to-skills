import pytest

from app.contracts.metadata_contract import MetadataItem


def test_fetch_all_servers_returns_only_servers(client):
    response = client.post(
        "/api/metadata/v1/fetch",
        json={"entity": "*", "field": ["NAME", "DESCRIPTION"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1

    entry = body[0]
    assert set(entry["fields"].keys()) == {"NAME", "DESCRIPTION"}
    assert entry["type"] == "server"
    assert entry["tool"] is None


def test_fetch_all_tools_returns_only_tools(client):
    response = client.post(
        "/api/metadata/v1/fetch",
        json={"entity": "*.*", "field": ["NAME", "DESCRIPTION"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1

    entry = body[0]
    assert set(entry["fields"].keys()) == {"NAME", "DESCRIPTION"}
    assert entry["type"] == "tool"
    assert entry["tool"]


def test_fetch_specific_server_single_field(client):
    response = client.post(
        "/api/metadata/v1/fetch",
        json={"entity": "chrome-devtools", "field": "NAME"},
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    entry = body[0]
    assert entry["type"] == "server"
    assert entry["fields"] == {"NAME": "chrome-devtools"}


def test_fetch_tools_wildcard_returns_tool_entry(client):
    response = client.post(
        "/api/metadata/v1/fetch",
        json={"entity": "chrome-devtools.*", "field": ["USAGE"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    entry = body[0]
    assert entry["type"] == "tool"
    assert entry["fields"] == {"USAGE": "uv run sample-command --tool"}


def test_fetch_entity_list_returns_data_for_known_pattern(client):
    response = client.post(
        "/api/metadata/v1/fetch",
        json={"entity": ["*", "chrome-devtools"], "field": ["NAME"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) >= 1


def test_unknown_server_pattern_returns_empty_list(client):
    response = client.post(
        "/api/metadata/v1/fetch",
        json={"entity": "nonexistent-server", "field": "NAME"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_unknown_tool_pattern_returns_empty_list(client):
    response = client.post(
        "/api/metadata/v1/fetch",
        json={"entity": "unknown.*", "field": ["NAME", "DESCRIPTION"]},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_extra_field_triggers_validation_error(client):
    response = client.post(
        "/api/metadata/v1/fetch",
        json={"entity": "*", "field": "NAME", "extra": "bad"},
    )

    assert response.status_code == 400
    body = response.json()
    assert body.get("body") is None
    assert "detail" in body
    assert isinstance(body["detail"], list)
    for entry in body["detail"]:
        assert isinstance(entry, dict)
        assert "ctx" in entry
        assert isinstance(entry["ctx"], dict)
        for ctx_value in entry["ctx"].values():
            assert isinstance(ctx_value, str)


def test_extra_field_includes_body_when_enabled(client_include_error_body):
    response = client_include_error_body.post(
        "/api/metadata/v1/fetch",
        json={"entity": "*", "field": "NAME", "extra": "bad"},
    )

    assert response.status_code == 400
    body = response.json()
    assert body.get("body") == {"entity": "*", "field": "NAME", "extra": "bad"}
    assert "detail" in body


@pytest.mark.parametrize("invalid_field", ["INVALID_FIELD"])
def test_invalid_field_literal_triggers_validation_error(client, invalid_field):
    response = client.post(
        "/api/metadata/v1/fetch",
        json={"entity": "*", "field": invalid_field},
    )

    assert response.status_code == 400
    body = response.json()
    assert "detail" in body
    assert isinstance(body["detail"], list)
    for entry in body["detail"]:
        assert isinstance(entry, dict)
        assert "msg" in entry
        assert "type" in entry


def test_empty_entity_string_triggers_validation_error(client):
    response = client.post(
        "/api/metadata/v1/fetch",
        json={"entity": "", "field": "NAME"},
    )

    assert response.status_code == 400
    body = response.json()
    assert "detail" in body
    assert isinstance(body["detail"], list)
    for entry in body["detail"]:
        assert isinstance(entry, dict)
        assert "msg" in entry
        assert "type" in entry


def test_empty_entity_list_triggers_validation_error(client):
    response = client.post(
        "/api/metadata/v1/fetch",
        json={"entity": [], "field": "NAME"},
    )

    assert response.status_code == 400
    body = response.json()
    assert "detail" in body
    assert isinstance(body["detail"], list)
    for entry in body["detail"]:
        assert isinstance(entry, dict)
        assert "msg" in entry
        assert "type" in entry


def test_response_items_validate_against_contract(client):
    response = client.post(
        "/api/metadata/v1/fetch",
        json={"entity": "*", "field": ["NAME", "DESCRIPTION", "USAGE"]},
    )

    assert response.status_code == 200
    for item in response.json():
        MetadataItem.model_validate(item)


def test_field_filtering_returns_only_requested_keys(client):
    response = client.post(
        "/api/metadata/v1/fetch",
        json={"entity": "chrome-devtools", "field": ["NAME"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert all(set(entry["fields"].keys()) == {"NAME"} for entry in body)
