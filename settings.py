from dotenv import dotenv_values


config = dotenv_values(".env")

TOKEN = config['TOKEN']
BD_STRING = config['BD_STRING']
GROUP_ID = config['GROUP_ID']
MEDIA_PATH = config['MEDIA_PATH']

API_VERSION = '5.120'
VK_CALLBACKS = ["show_snackbar", "open_link", "open_app"]
CHAT_URL = "https://vk.com/im?invite_chat_id=8589934592511158923&invite_link=7dy4cCHWGp8qjZYWNUmhh3D5AFIBEtVwbwo=&invite_hash=7dy4cCHWGp8qjQ=="
LIFE_SET_KEY = 60 * 5

