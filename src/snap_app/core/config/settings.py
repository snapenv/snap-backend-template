"""Snap FastStream Template settings."""

# BUILTIN modules
from functools import lru_cache

# Third party modules
from pydantic_settings import SettingsConfigDict

# SnapEnv base modules
from snap_core.config.manager import (
    SnapEnvCommonSettings,
)


class AppSettings(SnapEnvCommonSettings):
    """AppSettings app configuration parameters..

    Values from {ENVIRONMENT}.env supersede previous values when the file exists.

    Args
        SnapEnvCommonSettings (_type_): Configuração do APP.
    """

    # Debug
    APP_TITLE: str
    LOG_LEVEL: str

    model_config = SettingsConfigDict(env_file=f"{SnapEnvCommonSettings().env}.env")


@lru_cache
def get_settings() -> AppSettings:
    """get_settings _summary_.

    Returns
    -------
        AppSettings: _description_
    """
    return AppSettings()


settings: AppSettings = get_settings()
