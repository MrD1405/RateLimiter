from locust import HttpUser , task
import os
from pathlib import Path
from dotenv import load_dotenv

env_path=Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class HomePage(HttpUser):
    def on_start(self):
        token = os.getenv('TEST_USER_5_JWT_TOKEN')
        self.client.headers={"Authorization":f"Bearer {token}"}
    @task
    def homepage(self):
        self.client.get('/test')