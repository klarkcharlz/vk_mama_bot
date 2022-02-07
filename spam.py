import vk_api

from settings import TOKEN, API_VERSION
from function import write_msg, get_ids


vk_session = vk_api.VkApi(token=TOKEN, api_version=API_VERSION)
vk = vk_session.get_api()


if __name__ == "__main__":
    ids = get_ids()
    msg = "TEST"
    for id_ in ids:
        try:
            write_msg(vk, id_, msg)
        except Exception as err:
            print(f"{type(err)}\n{err}")
