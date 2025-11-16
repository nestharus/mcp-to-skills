"""Data contracts for the MCP Metadata Broker `/api/metadata/v1/fetch` endpoint.

The models defined here act as the public schema for the broker. They express how
clients request metadata (glob-like entity patterns plus desired fields) and how
the service responds with strongly typed server/tool entries. Invalid payloads are
normalized through FastAPI request validation and now return HTTP 400 errors so
clients receive standard bad-request semantics instead of the default 422.
"""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, model_validator
from pydantic import Field as PydanticField

type FieldLiteral = Literal[
    "NAME",
    "DESCRIPTION",
    "USAGE",
]
type _EntityList = Annotated[list[str], PydanticField(min_length=1, max_length=32)]
type _FieldList = Annotated[list[FieldLiteral], PydanticField(max_length=3)]
type Entity = str | _EntityList
type Field = FieldLiteral | _FieldList

MAX_METADATA_ITEMS = 100
MAX_VALIDATION_ERRORS = 32


class FetchRequest(BaseModel):
    """Request envelope for fetching metadata by entity pattern and fields.

    Attributes:
        entity: Glob-like selectors describing which servers/tools to match.
            Examples include "chrome-devtools" for a single server,
            "chrome-devtools.*" for every tool in that server, "*" for all
            servers, and "*.*" for all tools globally.
        field: Field literal(s) defining which metadata keys to return. The
            valid options are NAME (identifier), DESCRIPTION (human summary),
            and USAGE (parameters/examples). Validation rejects unknown values.

    Examples:
        FetchRequest(entity="chrome-devtools.*", field=["NAME", "DESCRIPTION"])  # noqa: E501
    """

    model_config = ConfigDict(extra="forbid")

    entity: Entity
    field: Field

    @model_validator(mode="after")
    def validate_entity_content(self):
        """Ensure entity selectors contain meaningful values."""

        def _invalid(value: str) -> bool:
            return value.strip() == ""

        if isinstance(self.entity, str):
            if _invalid(self.entity):
                raise ValueError("FetchRequest.entity must be a non-empty string")  # noqa: TRY003
        else:
            if not self.entity:
                raise ValueError("FetchRequest.entity list must not be empty")  # noqa: TRY003
            if any(_invalid(entry) for entry in self.entity):
                raise ValueError("FetchRequest.entity entries must be non-empty strings")  # noqa: TRY003
        return self


class MetadataItem(BaseModel):
    """Response entry encapsulating metadata for a server or tool.

    Attributes:
        type: Either "server" or "tool" to distinguish the payload variant.
        server: The parent server identifier, always populated.
        tool: Populated only when type == "tool"; server entries keep this as
            None.
        fields: Dictionary containing only the requested field keys (NAME,
            DESCRIPTION, USAGE) and their string values.

    Examples:
        MetadataItem(
            type="server",
            server="chrome-devtools",
            tool=None,
            fields={"NAME": "chrome-devtools", "DESCRIPTION": "Chrome tools"},
        )
        MetadataItem(
            type="tool",
            server="chrome-devtools",
            tool="console",
            fields={"USAGE": "uv run fetch metadata"},
        )
    """

    model_config = ConfigDict(extra="forbid")

    type: Literal["server", "tool"]
    server: str
    tool: str | None = None
    fields: dict[FieldLiteral, str]

    @model_validator(mode="after")
    def validate_tool_consistency(self):
        """Ensure `type` and `tool` remain semantically aligned.

        Prevents invalid payloads such as server entries with tool values or
        tool entries missing identifiers before responses leave the broker.

        Raises:
            ValueError: If server is an empty or whitespace-only string.
            ValueError: If a server entry includes a tool value or if a tool
                entry omits the tool identifier.

        Returns:
            MetadataItem: The validated instance for chaining.
        """

        if self.server.strip() == "":
            raise ValueError("MetadataItem.server must be a non-empty string")  # noqa: TRY003
        if self.type == "server" and self.tool is not None:
            raise ValueError("MetadataItem with type='server' must have tool=None")  # noqa: TRY003
        if self.type == "tool" and (self.tool is None or self.tool.strip() == ""):
            raise ValueError("MetadataItem with type='tool' must have a non-empty tool value")  # noqa: TRY003
        return self


type MetadataResponse = Annotated[
    list[MetadataItem],
    PydanticField(max_length=MAX_METADATA_ITEMS),
]
