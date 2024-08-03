"""Snap FastStream Template settings."""

# BUILTIN modules
from functools import lru_cache

# Third party modules
from pydantic import Field
from pydantic_settings import SettingsConfigDict

# SnapEnv base modules
from snap_core.config.manager import (
    ENVIRONMENT,
    MISSING_SECRET,
    SnapEnvCommonSettings,
)


class CommonSettings(SnapEnvCommonSettings):
    """CommonSettings _summary_.

    Args
        SnapEnvCommonSettings (_type_): _description_
    """

    # Debug
    # LOG_LEVEL: str

    # Secrets depending parameters.
    # service_api_key: str = Field(MISSING_SECRET, alias="service_api_key")


class DevSettings(CommonSettings):
    """Configuration parameters for DEV environment.

    Values from dev.env supersede previous values when the file exists.
    """

    model_config = SettingsConfigDict(env_file=f"{CommonSettings().env}.env")


class TestSettings(CommonSettings):
    """Configuration parameters for TEST environment.

    Values from test.env supersedes previous values when the file exists.
    """

    model_config = SettingsConfigDict(env_file=f"{CommonSettings().env}.env")


class StageSettings(CommonSettings):
    """Configuration parameters for STAGE environment.

    Values from stage.env supersede previous values when the file exists.
    """

    model_config = SettingsConfigDict(env_file=f"{CommonSettings().env}.env")


class ProdSettings(CommonSettings):
    """Configuration parameters for PROD environment.

    Values from prod.env supersedes previous values when the file exists.
    """

    model_config = SettingsConfigDict(env_file=f"{CommonSettings().env}.env")


# Translation table between ENVIRONMENT value and their classes.
_settings_setup = {
    "dev": DevSettings,
    "test": TestSettings,
    "stage": StageSettings,
    "prod": ProdSettings,
}


@lru_cache
def get_settings() -> DevSettings | TestSettings | StageSettings | ProdSettings:
    """get_settings _summary_.

    Returns
    -------
        Dev | Test | Prod | Stage: _description_
    """
    return _settings_setup[ENVIRONMENT]()


settings: DevSettings | TestSettings | StageSettings | ProdSettings = get_settings()
