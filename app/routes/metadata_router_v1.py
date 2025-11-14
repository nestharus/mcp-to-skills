from fastapi import APIRouter
from app.contracts.metadata_contract import MetadataItem

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/sample", response_model=MetadataItem)
async def sample_item() -> MetadataItem:
    return MetadataItem(type="server", server="example", fields={"NAME": "example"})
