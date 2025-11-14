from typing import Literal

from pydantic import BaseModel, model_validator

type FieldLiteral = Literal["NAME", "DESCRIPTION", "USAGE"]

type Entity = str | list[str]
type Field = FieldLiteral | list[FieldLiteral]


class FetchRequest(BaseModel):
    entity: Entity
    field: Field


class MetadataItem(BaseModel):
    type: Literal["server", "tool"]
    server: str
    tool: str | None = None
    fields: dict[str, str]

    @model_validator(mode="after")
    def validate_tool_consistency(self):
        if self.type == "server" and self.tool is not None:
            raise ValueError("MetadataItem with type='server' must have tool=None")
        if self.type == "tool" and self.tool is None:
            raise ValueError("MetadataItem with type='tool' must have a non-None tool value")
        return self
