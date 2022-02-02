import re
from time import sleep

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from requests.exceptions import ReadTimeout, ConnectionError

from keyboard import start_button, born_keyboard
from settings import TOKEN, API_VERSION, GROUP_ID, VK_CALLBACKS, IGNORE_CHAR
from controller import ACTION, MES_COM
from function import (custom_event_response,
                      vk_callback_event_response,
                      get_user_name_from_vk_id,
                      write_msg,
                      validate_day_born,
                      calculate_day_born)
from bd import r, next_collection

vk_session = vk_api.VkApi(token=TOKEN, api_version=API_VERSION)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)


if __name__ == "__main__":
    next_collection.delete_many({})  # очистка монго при старте бота, нужна ли ?
    print("Server started")
    while True:
        try:
            for event in longpoll.listen():
                # print(event.type)
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if event.from_user:
                        print(event.obj.message.keys())
                        mes_text = event.obj.message["text"]
                        id_ = event.obj.message["from_id"]
                        if mes_text.lower().strip() == "начать":
                            print(f'New message for me by {get_user_name_from_vk_id(id_)}:\n'
                                  f'{mes_text}')
                            write_msg(vk, id_,
                                      f'Приветствую {get_user_name_from_vk_id(id_)}. Ты знаешь дату родов ?',
                                      born_keyboard)
                        elif re.match(r"\d{2}.\d{2}.\d{4}", mes_text):
                            print("DATA SET")  # check redis
                            mode = r.get(str(id_))
                            if mode:
                                mode = mode.decode("utf-8")
                            print(mode)
                            if mode == "born":
                                validate_day_born(mes_text, id_, vk)
                            elif mode == "blood":
                                calculate_day_born(mes_text, id_, vk)
                            else:
                                print("User not in set mode!")
                        elif mes_text.strip().lower().rstrip(IGNORE_CHAR) in MES_COM.keys():
                            MES_COM[mes_text.strip().lower().rstrip(IGNORE_CHAR)](vk, id_)
                        else:
                            write_msg(vk, event.obj.message["from_id"],
                                      "Я вас не понимаю, нажмите кнопку.",
                                      start_button)
                elif event.type == VkBotEventType.MESSAGE_EVENT:
                    # print(event.object.payload)
                    if event.object.payload['type'] in ACTION.keys():
                        print(f'Start {event.object.payload["type"]}')
                        custom_event_response(vk, event)
                        ACTION[event.object.payload['type']](vk, event.object.user_id)
                    elif event.object.payload['type'] in VK_CALLBACKS:
                        # print(event.object.payload)
                        vk_callback_event_response(vk, event)
        except (ReadTimeout, ConnectionError):
            while True:
                try:
                    print("Переподключение к серверам ВК.")
                    vk_session = vk_api.VkApi(token=TOKEN, api_version=API_VERSION)
                    vk = vk_session.get_api()
                    longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
                except Exception as err:
                    print("Переводключение неудачно")
                    sleep(10)
                else:
                    break
