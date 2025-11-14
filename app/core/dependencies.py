from app.core.settings import Settings


_settings_cache: dict[bool, Settings] = {}


def get_settings(*, allow_missing_config: bool = False) -> Settings:
    """Return cached Settings respecting validation mode."""
    if allow_missing_config not in _settings_cache:
        _settings_cache[allow_missing_config] = Settings(
            allow_missing_config=allow_missing_config
        )
    return _settings_cache[allow_missing_config]
