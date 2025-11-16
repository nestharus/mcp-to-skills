from app.contracts.metadata_contract import MetadataItem
from app.routes import metadata_router_v1


def test_dedupe_and_limit_caps_results_at_max_items():
    items = [
        MetadataItem(type="server", server=f"server-{i}", fields={"NAME": f"server-{i}"})
        for i in range(150)
    ]

    limited = metadata_router_v1._dedupe_and_limit(items)

    assert len(limited) == 100
    assert limited[0].server == "server-0"
    assert limited[-1].server == "server-99"
