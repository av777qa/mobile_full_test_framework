import requests
from config import BASE_URL, OCTOPUS_EMAIL, OCTOPUS_PASSWORD


class AuthClient:
    def __init__(self):
        self.email = OCTOPUS_EMAIL
        self.password = OCTOPUS_PASSWORD
        self.token = None

    def login(self) -> str:
        url = f"{BASE_URL}/api/sanctum/login"
        payload = {"email": self.email, "password": self.password}
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        self.token = resp.json()["data"]["token"]["accessToken"]
        return f"Bearer {self.token}"
