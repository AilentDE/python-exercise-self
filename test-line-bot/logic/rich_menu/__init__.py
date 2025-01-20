import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from config.setting import LineMessageSetting
from logic.rich_menu.schema_sample import RichmenuSample


class RichMenuLogic:

    _url: str = "https://api.line.me/v2/bot/richmenu"
    _data_url: str = "https://api-data.line.me/v2/bot/richmenu"
    _session: requests.Session

    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {LineMessageSetting.access_token}",
            }
        )

    def __del__(self):
        self._session.close()

    def get_richmenu_list(self) -> list[dict]:
        url = self._url + "/list"
        r = self._session.get(url)
        return r.json()["richmenus"]

    def get_richmenu_alias(self) -> list[dict]:
        url = self._url + "/alias/list"
        r = self._session.get(url)
        return r.json()["aliases"]

    def create_richmenu(self, richmenu: dict) -> str:
        r = self._session.post(self._url, json=richmenu)
        return r.json()["richMenuId"]

    def upload_image(self, richmenu_id: str, image_path: str):
        url = self._data_url + f"/{richmenu_id}/content"
        with open(image_path, "rb") as f:
            headers = self._session.headers.copy()
            headers.update({"Content-Type": "image/png"})
            r = self._session.post(url, headers=headers, data=f)
            r.raise_for_status()

    def delete_richmenu(self, richmenu_id: str):
        url = self._url + f"/{richmenu_id}"
        r = self._session.delete(url)
        r.raise_for_status()

    def create_richmenu_alias(self, richmenu_id: str, alias_id: str):
        url = self._url + "/alias"
        data = {
            "richMenuId": richmenu_id,
            "richMenuAliasId": alias_id,
        }
        r = self._session.post(url, json=data)
        r.raise_for_status()

    def delete_richmenu_alias(self, alias_id: str):
        url = self._url + f"/alias/{alias_id}"
        r = self._session.delete(url)
        r.raise_for_status()

    def set_default_richmenu(self, richmenu_id: str):
        url = f"https://api.line.me/v2/bot/user/all/richmenu/{richmenu_id}"
        r = self._session.post(url)
        r.raise_for_status()


class SampleRichMenu(RichMenuLogic):

    def clear_assets(self):
        richmenus = self.get_richmenu_list()
        alias = self.get_richmenu_alias()

        with ThreadPoolExecutor(max_workers=5) as executor:
            threads = []
            for richmenu in richmenus:
                threads.append(executor.submit(self.delete_richmenu, richmenu["richMenuId"]))
            for alias in alias:
                threads.append(executor.submit(self.delete_richmenu_alias, alias["richMenuAliasId"]))

            for future in as_completed(threads):
                try:
                    future.result()
                except Exception as ex:
                    print("Failed to delete richmenu", ex)

    def create_sample_richmenu(self):
        richmenu_schemas = (
            ("login", RichmenuSample.login[0]),
            ("without_login", RichmenuSample.without_login[0]),
        )
        default_richmenu_id = ""

        for menu_type, menu in richmenu_schemas:
            for tab, schema in menu.items():
                richmenu_id = self.create_richmenu(schema)
                if menu_type == "without_login" and tab == "tab_b":
                    default_richmenu_id = richmenu_id
                self.upload_image(richmenu_id, RichmenuSample.asset_path[0][menu_type][tab])
                self.create_richmenu_alias(richmenu_id, schema["name"])

        self.set_default_richmenu(default_richmenu_id)
