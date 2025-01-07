import requests
from config.setting import ChannelSetting


class WebhookReplay:
    """Webhook replay.

    Attributes:
        _url (str): The Line API base URL.
        _token (str): The Line Official Account token.
        _session (requests.Session): The session.
        chat_id (str): The chat (user) ID.
    """

    _url: str = "https://api.line.me/v2/bot"
    _token: str = ChannelSetting.access_token
    _session: requests.Session
    chat_id: str

    def __init__(self, chat_id: str):
        """Initialize the WebhookReplay with a chat ID and set up the session.

        Args:
            chat_id (str): The chat (user) ID.
        """
        self.chat_id = chat_id
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {self._token}",
            }
        )
        self.chat_id = chat_id

    def start_loading_animation(self, delay: int = 10) -> None:
        """Start a loading animation.

        Args:
            delay (int): The delay in seconds.
        """
        url = self._url + "/chat/loading/start"
        data = {"chatId": self.chat_id, "loadingSeconds": delay}
        response = self._session.post(url, json=data)
        print("animation", response.text)

    def reply_text(self, reply_token: str, text: str) -> None:
        """Reply with text.

        Args:
            reply_token (str): The reply token.
            text (str): The text to reply with.
        """
        url = self._url + "/message/reply"
        data = {
            "replyToken": reply_token,
            "messages": [
                {"type": "text", "text": text},
            ],
        }
        response = self._session.post(url, json=data)
        print("reply", response.text)
