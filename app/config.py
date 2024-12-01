from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix=False,
    settings_files=["configs/settings.toml"],
    secrets="configs/.secrets.toml",
    environments=True,
    load_dotenv=False,
    merge_enabled=True,
)
