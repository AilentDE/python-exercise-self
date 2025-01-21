import requests

from config.setting import LineLoginSetting


class LineLoginLogic:

    _url: str = "https://api.line.me/oauth2/v2.1/token"
    _session: requests.Session

    def __init__(self):
        self._session = requests.Session()

    def __del__(self):
        self._session.close()

    def get_access_token(self, code: str) -> dict:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": LineLoginSetting.redirect_uri,
            "client_id": LineLoginSetting.cid,
            "client_secret": LineLoginSetting.secret,
        }
        r = self._session.post(self._url, headers=headers, data=data)
        r.raise_for_status()

        return {
            "access_token": r.json()["access_token"],
            "refresh_token": r.json()["refresh_token"],
            "id_token": r.json()["id_token"],
        }
