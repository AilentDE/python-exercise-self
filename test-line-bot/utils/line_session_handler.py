import requests

from config.setting import LineMessageSetting


def get_line_session():
    with requests.Session() as session:
        session.headers.update(
            {"Authorization": f"Bearer {LineMessageSetting.access_token}", "Content-Type": "application/json"}
        )
        return session
