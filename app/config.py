from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    wc_app_id: str = 'wx44c5f6266913817e'
    wc_app_secret: str = ''
    wc_cpi_bin_api: str = 'https://api.weixin.qq.com/cgi-bin'
    llm_base_url: str = 'https://api.deepseek.com'
    llm_api_key: str = ''
    llm_model: str = 'deepseek-chat'


settings = Settings()
