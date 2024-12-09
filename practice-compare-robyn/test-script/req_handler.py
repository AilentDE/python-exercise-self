from loguru import logger
from faker import Faker
import subprocess
import requests


class TestHandler:
    _url = "http://localhost:8000"
    _api_name = ""

    def __init__(self, api_name: str) -> None:
        self._api_name = api_name

    def home(self):
        try:
            result = subprocess.run(
                ["oha", "--disable-keepalive", "--json", self._url], capture_output=True, text=True, check=True
            )
            with open(f"home_{self._api_name}.json", "w") as f:
                f.write(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"subprocess failure：{e}")

    def visit_message(self, access_token: str, message_id: str):
        try:
            result = subprocess.run(
                [
                    "oha",
                    "--disable-keepalive",
                    "--json",
                    "-H",
                    f"Authorization: Bearer {access_token}",
                    f"{self._url}/message/{message_id}/auth",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            with open(f"message_{self._api_name}.json", "w") as f:
                f.write(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"subprocess failure：{e}")

    def delete_message(self, access_token: str, message_id: str):
        try:
            result = subprocess.run(
                [
                    "oha",
                    "--disable-keepalive",
                    "--json",
                    "-m",
                    "DELETE",
                    "-H",
                    f"Authorization: Bearer {access_token}",
                    f"{self._url}/message/{message_id}/delete",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            with open(f"delete_{self._api_name}.json", "w") as f:
                f.write(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"subprocess failure：{e}")


class UserGenerator:
    fake = Faker()
    _url = "http://localhost:8000"
    username = ""
    password = ""
    email = ""
    access_token = ""
    user_id = ""
    _api_type = ""

    def __init__(self, api_name) -> None:
        self.username = self.fake.user_name()
        self.password = self.fake.password()
        self.email = self.fake.email()
        self._api_type = api_name

        r = requests.post(
            self._url + '/auth/register',
            json={"username": self.username, "password": self.password, "email": self.email},
        )
        self.access_token = r.json()["data"]["accessToken"]

    def create_message(self) -> str:
        title = self.fake.name()
        content = self.fake.text()

        r = requests.post(
            self._url + "/message/create",
            json={"title": title, "content": content, "permission_level": 1},
            headers={"Authorization": "Bearer " + self.access_token},
        )
        if self._api_type == "robyn":
            self.user_id = r.json()["data"]["message"]["authorId"]
            return r.json()["data"]["message"]["id"]
        else:
            self.user_id = r.json()["data"]["authorId"]
            return r.json()["data"]["id"]

    def delete_message(self, message_id: str) -> None:
        _ = requests.delete(
            self._url + f"/message/{message_id}/delete", headers={"Authorization": "Bearer " + self.access_token}
        )

    def subscribe_user(self, target_id: str) -> None:
        _ = requests.post(
            self._url + f"/subscribe/{target_id}/join", headers={"Authorization": "Bearer " + self.access_token}
        )
