from config.setting import ChannelSetting
from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import AsyncApiClient, AsyncMessagingApi, Configuration


class LineBoteState:

    parser = WebhookParser
    api: AsyncMessagingApi | None

    def __init__(self):
        self.parser = WebhookParser(ChannelSetting.secret)
        self.api = None

    def generate_api(self):
        configuration = Configuration(access_token=ChannelSetting.access_token)
        async_api_client = AsyncApiClient(configuration)
        self.api = AsyncMessagingApi(async_api_client)


line_bot_state = LineBoteState()
