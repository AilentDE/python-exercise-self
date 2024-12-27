import requests

from config.setting import ChannelSetting


def get_line_session():
    with requests.Session() as session:
        session.headers.update({
            "Authorization": f"Bearer {ChannelSetting.access_token}",
            "Content-Type": "application/json"
        })
        return session
