"""Validation coverage for metadata contract models."""

import pytest
from pydantic import ValidationError

from app.contracts.metadata_contract import FetchRequest, MetadataItem


def test_fetch_request_rejects_extra_keys():
    """Unknown payload keys should cause validation to fail."""

    with pytest.raises(ValidationError):
        FetchRequest.model_validate({"entity": "*", "field": "NAME", "unexpected": "value"})


def test_fetch_request_accepts_valid_payload():
    """Valid payloads should create FetchRequest instances."""

    request = FetchRequest.model_validate({"entity": "*", "field": ["NAME", "DESCRIPTION"]})

    assert request.entity == "*"
    assert "NAME" in request.field
    assert "DESCRIPTION" in request.field


def test_fetch_request_accepts_entity_list():
    """List-based entity selector should validate."""

    request = FetchRequest.model_validate({"entity": ["alpha", "beta"], "field": ["NAME"]})

    assert request.entity == ["alpha", "beta"]


def test_fetch_request_rejects_empty_entity_list():
    """Empty entity lists should be rejected."""

    with pytest.raises(ValidationError):
        FetchRequest.model_validate({"entity": [], "field": ["NAME"]})


def test_fetch_request_rejects_entity_list_with_empty_entry():
    """Entity list entries must be non-empty strings."""

    with pytest.raises(ValidationError):
        FetchRequest.model_validate({"entity": ["alpha", " "], "field": ["NAME"]})


def test_fetch_request_rejects_unknown_field_literal():
    """Unknown field literals should be rejected."""

    with pytest.raises(ValidationError):
        FetchRequest.model_validate({"entity": "*", "field": ["NAME", "UNKNOWN"]})


def test_metadata_item_accepts_known_fields_only():
    item = MetadataItem(type="server", server="alpha", tool=None, fields={"NAME": "alpha"})

    assert item.fields == {"NAME": "alpha"}


def test_metadata_item_accepts_tool_with_standard_fields():
    item = MetadataItem(
        type="tool",
        server="alpha",
        tool="beta",
        fields={"NAME": "beta", "DESCRIPTION": "tool beta description"},
    )

    assert item.type == "tool"
    assert item.server == "alpha"
    assert item.tool == "beta"
    assert item.fields["NAME"] == "beta"
    assert item.fields["DESCRIPTION"] == "tool beta description"


def test_metadata_item_rejects_unknown_field_key():
    with pytest.raises(ValidationError):
        MetadataItem(
            type="server",
            server="alpha",
            tool=None,
            fields={
                "NAME": "alpha",
                "EXTRA": "nope",
            },
        )


def test_metadata_item_rejects_server_with_tool():
    with pytest.raises(ValidationError):
        MetadataItem(
            type="server",
            server="alpha",
            tool="should-be-none",
            fields={"NAME": "alpha"},
        )


def test_metadata_item_rejects_tool_without_tool_name():
    with pytest.raises(ValidationError):
        MetadataItem(
            type="tool",
            server="alpha",
            tool=None,
            fields={"NAME": "alpha"},
        )


def test_metadata_item_accepts_empty_fields_dict():
    item = MetadataItem(type="server", server="alpha", tool=None, fields={})

    assert item.fields == {}


def test_metadata_item_rejects_empty_server_string():
    with pytest.raises(ValidationError):
        MetadataItem(type="server", server="", tool=None, fields={"NAME": "alpha"})


def test_fetch_request_rejects_empty_entity_string():
    with pytest.raises(ValidationError):
        FetchRequest.model_validate({"entity": "", "field": "NAME"})
