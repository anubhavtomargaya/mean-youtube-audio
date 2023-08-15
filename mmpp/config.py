from  pydantic_settings import BaseSettings
#pip install pydantic-settings
from download import MetaInfo

class Settings(BaseSettings):
    # DEFAULT_VAR="some default string value"  # default value if env variable does not exist
    ACTIVE_PID: int = 0
    ACTIVE_TITLE:str='null'
    APP_MAX: int=100 # default value if env variable does not exist

# global instance
settings = Settings()
class Now(BaseSettings):
    # DEFAULT_VAR="some default string value"  # default value if env variable does not exist
    ACTIVE_PID: int = 0
    # META:MetaInfo=None
    
# global instance
settings = Settings()
# now = Now()