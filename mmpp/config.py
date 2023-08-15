from  pydantic_settings import BaseSettings
#pip install pydantic-settings


class Settings(BaseSettings):
    # DEFAULT_VAR="some default string value"  # default value if env variable does not exist
    ACTIVE_PID: int = 0
    ACTIVE_TITLE:str='null'
    APP_MAX: int=100 # default value if env variable does not exist

# global instance
settings = Settings()