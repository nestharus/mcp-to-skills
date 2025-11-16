from fastapi import APIRouter

from app.contracts.metadata_contract import (
    MAX_METADATA_ITEMS,
    MAX_VALIDATION_ERRORS,
    FetchRequest,
    FieldLiteral,
    MetadataItem,
    MetadataResponse,
)

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/sample", response_model=MetadataItem)
async def sample_item() -> MetadataItem:
    return MetadataItem(type="server", server="example", fields={"NAME": "example"})


def _normalize_entity_list(value: str | list[str]) -> list[str]:
    return value if isinstance(value, list) else [value]


def _normalize_field_list(value: FieldLiteral | list[FieldLiteral]) -> list[FieldLiteral]:
    return value if isinstance(value, list) else [value]


def _filter_fields(
    requested: list[FieldLiteral], *, name: str, description: str, usage: str
) -> dict[FieldLiteral, str]:
    sample_values: dict[FieldLiteral, str] = {
        "NAME": name,
        "DESCRIPTION": description,
        "USAGE": usage,
    }
    return {field: sample_values[field] for field in requested if field in sample_values}


def _dedupe_and_limit(
    items: list[MetadataItem], *, max_items: int = MAX_METADATA_ITEMS
) -> list[MetadataItem]:
    seen: set[tuple[str, str, str | None]] = set()
    unique_items: list[MetadataItem] = []

    for item in items:
        key = (item.type, item.server, item.tool)
        if key in seen:
            continue
        seen.add(key)
        unique_items.append(item)
        if len(unique_items) >= max_items:
            break

    return unique_items


@router.post(
    "/fetch",
    response_model=MetadataResponse,
    summary="Fetch MCP metadata by pattern",
    description=(
        "Fetch metadata for MCP servers and tools using glob-like selectors.\n\n"
        "Examples: `chrome-devtools` targets a single server, `chrome-devtools.*`"
        " retrieves every tool in that server, `*` returns all servers, and `*.*`"
        " expands to every tool globally. Pass `field` as a string or list to filter"
        " the metadata keys you want returned; only requested keys appear in"
        " the response `fields` object."
    ),
    responses={
        200: {"description": "Matching servers/tools with requested fields"},
        400: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "array",
                                "maxItems": MAX_VALIDATION_ERRORS,
                                "items": {"type": "string"},
                            },
                            "body": {},
                        },
                        "required": ["detail", "body"],
                    }
                }
            },
        },
    },
)
async def fetch_metadata(request: FetchRequest) -> MetadataResponse:
    # Note: Currently returns hardcoded sample data for scaffolding purposes. Real
    # metadata source integration (MCP server connection/registry) will be implemented
    # in a future PR with dynamic server/tool discovery and glob pattern matching.
    entity_patterns = _normalize_entity_list(request.entity)
    requested_fields = _normalize_field_list(request.field)

    def server_item(server: str, *, description: str) -> MetadataItem:
        return MetadataItem(
            type="server",
            server=server,
            fields=_filter_fields(
                requested_fields,
                name=server,
                description=description,
                usage="uv run sample-command",
            ),
        )

    def tool_item(server: str, tool: str, *, description: str) -> MetadataItem:
        return MetadataItem(
            type="tool",
            server=server,
            tool=tool,
            fields=_filter_fields(
                requested_fields,
                name=tool,
                description=description,
                usage="uv run sample-command --tool",
            ),
        )

    results: list[MetadataItem] = []
    for selector in entity_patterns:
        if selector == "*":
            results.append(server_item("sample-server", description="Sample server description"))
        elif selector == "*.*":
            results.append(
                tool_item("sample-server", "sample-tool", description="Sample tool description")
            )
        elif selector == "chrome-devtools":
            results.append(server_item("chrome-devtools", description="Chrome DevTools MCP server"))
        elif selector.startswith("chrome-devtools."):
            results.append(
                tool_item("chrome-devtools", "console", description="Chrome DevTools console tool")
            )

    return _dedupe_and_limit(results)
