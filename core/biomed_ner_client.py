import os

import requests


class MedicalNERClient:
    def __init__(self):
        host = os.getenv("BIOMED_HOST")
        if not host:
            raise ValueError("Environment variable 'BIOMED_HOST' must be set.")
        scheme = os.getenv("BIOMED_SCHEME", "http")
        self.api_url = f"{scheme}://{host}"

    def find_active_ingredients(self, text):
        """
        Sends text to the API and retrieves recognized entities.
        """
        response = requests.post(f"{self.api_url}/extract_entities", json={"text": text})
        if response.status_code != 200:
            raise RuntimeError(
                f"API call failed with status {response.status_code}: {response.text}"
            )
        result = [entity["text"] for entity in response.json()["entities"]]
        return result
