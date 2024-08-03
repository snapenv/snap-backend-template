"""SnapEnv settings."""

# BUILTIN modules
import os
import platform
import site
import sys

# Third party modules
from pydantic import computed_field
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict

# Constants
MISSING_ENV = ">>> undefined ENV parameter <<<"
MISSING_SECRET = ">>> missing SECRETS file <<<"
SECRETS_DIR = "/run/secrets" if os.path.exists("/.dockerenv") else f"{site.USER_BASE}/secrets"
PLATFORM = {"linux": "Linux", "linux2": "Linux", "win32": "Windows", "darwin": "MacOS"}
# ENVIRONMENT = os.getenv("ENVIRONMENT", MISSING_ENV)
ENVIRONMENT = os.getenv("ENVIRONMENT", "")


# --------------------------------------------------------------
# This needs to be done before the Base class gets evaluated, and
# to avoid getting five UserWarnings that the path does not exist.
#
# Create the directory if it does not already exist. When running
# inside Docker, skip it (Docker handles that just fine on its own).
#
if not os.path.exists("/.dockerenv"):
    os.makedirs(SECRETS_DIR, exist_ok=True)


# ------------------------------------------------------------------------
#
class SnapEnvCommonSettings(BaseSettings):
    r"""SnapEnv common configuration parameters shared between all environments.

    Read configuration parameters defined in this class, and from
    ENVIRONMENT variables and from the .env file.

    The source priority is changed (from default) to the following
    order (from highest to lowest):
      - env_settings
      - dotenv_settings
      - init_settings
      - file_secret_settings

    The following environment variables should already be defined:
      - HOSTNAME (on Linux servers only - set by OS)
      - COMPUTERNAME (on Windows servers only - set by OS)
      - ENVIRONMENT (on all servers)

    Path where your <environment>.env file should be placed:
      - linux: /home/<user>/.local
      - darwin: /home/<user>/.local
      - win32: C:\\Users\\<user>\\AppData\\Roaming\\Python'

    Path where your secret files should be placed:
      - linux: /home/<user>/.local/secrets
      - darwin: /home/<user>/.local/secrets
      - win32: C:\\Users\\<user>\\AppData\\Roaming\\Python\\secrets'
    """

    model_config = SettingsConfigDict(
        extra="ignore",
        secrets_dir=SECRETS_DIR,
        env_file_encoding="utf-8",
        env_file=".env",
    )

    # constant parameters.

    # Environment depending parameters.
    env: str = ENVIRONMENT
    platform: str = PLATFORM.get(sys.platform, "other")

    @computed_field  # type: ignore[misc]
    @property
    def server(self) -> str:
        """Return local server name stripped of possible domain part.

        :return: Server name in upper case.
        """
        return platform.node()

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Change source priority order (env trumps environment)."""
        return (env_settings, dotenv_settings, init_settings, file_secret_settings)
