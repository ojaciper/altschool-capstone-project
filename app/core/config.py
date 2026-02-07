from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    PROJECT_NAME:str = "FastApi Course Enrollment Managment"
    API_V1_STR:str = "/api/v1"
    
    
    # DATABASE
    DATABASE_URL:str
    
    
    # security
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 15
    ALGORITHM:str = ""
    SECRET_KEY:str = ""
    
    class Config:
        env_file = ".env"
        env_file_encoding ="utf-8"
        
        
settings = Setting()