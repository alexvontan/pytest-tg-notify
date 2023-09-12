from helpers.readers import read_yaml


class Config:
    def __init__(self):
        conf = read_yaml('config.yaml')
        self.bot_token = conf['bot_token']
        self.bot_chat_id = conf['bot_chat_id']
