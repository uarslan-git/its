import os
import dotenv
class Config:
    """Configuration for different environments for the api to run in.
    """
    def __init__(self):
        self.load_config()

    def load_config(self):
        # Get the value of the "env" environment variable, defaulting to "development"
        env = os.environ.get("ITS_ENV", "development")
        
        self.database_usr = "backend_service_user"

        if env == "development":
            dotenv.load_dotenv(dotenv.find_dotenv())
            self.database_pwd = os.environ.get("DB_SERVICE_PW")
            self.database_host = "localhost"
            self.database_port = 27017
            self.judge0_host = "localhost"

        elif env == "production":
            self.database_pwd = os.environ.get("DB_SERVICE_PW")
            self.database_host = "mongodb"
            self.database_port = 27017
            self.judge0_host = "j0-server"

        elif env == "staging":
            self.database_pwd = os.environ.get("DB_SERVICE_PW")
            self.database_host = "mongodb"
            self.database_port = 27017
            self.judge0_host = "j0-server"

        else:
            raise ValueError("Invalid 'env' value. Supported values are 'development', 'production', and 'staging'.")

config = Config()
