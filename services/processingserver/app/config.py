from dynaconf import Dynaconf

settings = Dynaconf(
    environments=True,  # activate layered environments
    envvar_prefix="DAMAE",  # export env. variables with `export DESTRA_FOO=bar`
    settings_files=["settings.toml"],  # load these files in the order
    env_switcher="DAMAE_ENV",  # `export DESTRA_ENV=production`
)
