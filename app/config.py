from dynaconf import Dynaconf

from app.schemas.indexes import OpenSearchIndexes

settings = Dynaconf(
    envvar_prefix=False,
    settings_files=["configs/settings.toml"],
    secrets="configs/.secrets.toml",
    environments=True,
    load_dotenv=False,
    merge_enabled=True,
)

OPEN_SEARCH_INDEXES = OpenSearchIndexes(**settings.INDEX_NAME)