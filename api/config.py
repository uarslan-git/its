import os

class Config:
    """Configuration for different environments for the api to run in.
    """
    def __init__(self):
        self.load_config()

    def load_config(self):
        # Get the value of the "env" environment variable, defaulting to "development"
        env = os.environ.get("env", "development")

        if env == "development":
            self.database_host = "localhost"
            self.database_port = 27017


        elif env == "production":
            self.database_host = "mongodb"
            self.database_port = 27017


        elif env == "staging":
            self.database_host = "mongodb"
            self.database_port = 27017


        else:
            raise ValueError("Invalid 'env' value. Supported values are 'development', 'production', and 'staging'.")

config = Config()
