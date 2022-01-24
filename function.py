import random
import json
from datetime import datetime, timedelta
from math import ceil

import requests
import bs4
from vk_api import VkUpload

from bd import session
from models import UsersUser, ContentContent, ContentAboutchildren
from settings import MEDIA_PATH
from keyboard import main_keyboard, start_button, settings_keyboard, born_keyboard


def get_user(vk, id_, check=True):
    model = session.query(UsersUser).filter(UsersUser.user_vk_id == id_).first()
    if not model and check:
        write_msg(vk, id_, "Вас нет в базе данных!")
        return None
    return model


def get_users_due_date(vk, id_, check=True):
    model = get_user(vk, id_, check)
    if model and not model.due_date and check:
        write_msg(vk, id_, "Дата родов не установлена!")
        return None
    elif model and model.due_date:
        return model.due_date


def custom_event_response(vk, event):
    vk.messages.sendMessageEventAnswer(
        event_id=event.object.event_id,
        user_id=event.object.user_id,
        peer_id=event.object.peer_id)


def vk_callback_event_response(vk, event):
    vk.messages.sendMessageEventAnswer(
        event_id=event.object.event_id,
        user_id=event.object.user_id,
        peer_id=event.object.peer_id,
        event_data=json.dumps(event.object.payload))


def get_user_name_from_vk_id(user_id):
    headers = {"Accept-Language": "ru"}
    request = requests.get("https://vk.com/id" + str(user_id), headers=headers)
    bs = bs4.BeautifulSoup(request.text, "html.parser")
    user_name = clean_all_tag_from_str(bs.findAll("title")[0])
    return " ".join(user_name.split()[:2])


def clean_all_tag_from_str(string_line):
    result = ""
    not_skip = True
    for i in list(string_line):
        if not_skip:
            if i == "<":
                not_skip = False
            else:
                result += i
        else:
            if i == ">":
                not_skip = True
    return result


def write_msg(vk, id_, message, keyboard_=None, img_path=None):
    data = dict(user_id=id_,
                peer_id=id_,
                random_id=random.getrandbits(32),
                message=message)
    if keyboard_:
        data["keyboard"] = keyboard_.get_keyboard()
    if img_path:
        upload = VkUpload(vk)
        photo = upload.photo_messages(img_path)
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        # data["attachment"] = attachment
        vk.messages.send(peer_id=id_, random_id=random.getrandbits(32), attachment=attachment)
    vk.messages.send(**data)


def insert_date(date, id_, vk):
    try:
        days, weeks = calculate_week_and_day(date)
    except ValueError:
        write_msg(vk, id_, f"Невалидная дата родов {date.strftime('%d.%m.%Y')}.")
    else:
        print(f"Записываю в базу данных дату родов {date} для пользователя {id_}.")

        user = UsersUser(user_vk_id=id_, due_date=date)

        model = session.query(UsersUser).filter(UsersUser.user_vk_id == id_).first()
        if model:
            session.query(UsersUser).filter(UsersUser.user_vk_id == id_).update({UsersUser.due_date: date})
            print("Model UPDATE")
        else:
            print("Model CREATE")
            session.add(user)
        session.commit()
        write_msg(vk, id_, f"Вы изменили дату родов.\nВаша дата родов: {date.strftime('%d.%m.%Y')}."
                           f"\nВы беремены {weeks} {declination(weeks, ['неделю', 'недели', 'недель'])}.\n"
                           f"До родов {days} {declination(days, ['день', 'дня', 'дней'])}.",
                  keyboard_=settings_keyboard)


def set_sub(id_, value):
    session.query(UsersUser).filter(UsersUser.user_vk_id == id_).update({UsersUser.subscribe: value})
    session.commit()
    print("Model UPDATE")


def calculate_day_born(date, id_, vk):
    print(f"дата месячных {date}.Расссчет даты родов....")
    try:
        calculate_date = datetime.strptime(date, "%d.%m.%Y").date() + timedelta(days=280)
    except Exception as err:
        err_text = f"Невалидная дата {date.strftime('%d.%m.%Y')}."
        print(err_text)
        write_msg(vk, id_, err_text)
    else:
        print(f"Рассчитанная дата: {calculate_date}")
        insert_date(calculate_date, id_, vk)  # запись


def validate_day_born(date, id_, vk):
    print(f"Дата родов {date}.Валидация даты родов....")
    try:
        born_date = datetime.strptime(date, "%d.%m.%Y").date()
    except Exception as err:
        err_text = f"Невалидная дата {date}."
        print(err_text)
        write_msg(vk, id_, err_text)
    else:
        print(f"Валидная дата: {born_date}")
        insert_date(born_date, id_, vk)  # запись


def calculate_week_and_day(date):
    today_date = datetime.now().date()
    # дней до родов
    days_to_born = (date - today_date).days
    # print(f"Дней до родов {days_to_born}")
    # недель от начала беременности
    weeks = ceil((today_date - (date - timedelta(days=280))).days / 7)
    # print(f"Вы беремены {weeks} недель.")
    if not (1 <= weeks <= 43) or days_to_born < 0:
        raise ValueError("invalid date")
    return days_to_born, weeks


def get_main_content(week, flag, day=None):
    model = session.query(ContentContent).filter(ContentContent.week == week,
                                                 ContentContent.parent_flag == flag).first()
    return f"{model.title}\n{model.text.replace('<br>', '')}", f"{MEDIA_PATH}/{model.src}"


def about_children(vk, id_):
    due_date = get_users_due_date(vk, id_, False)
    if due_date:
        days_to_born, weeks = calculate_week_and_day(due_date)
        children_content = session.query(ContentAboutchildren).filter(ContentAboutchildren.week == weeks).first()
        message = f"Вы беремены {weeks} {declination(weeks, ['неделю', 'недели', 'недель'])}." \
                  f"\nДо родов {days_to_born} {declination(days_to_born, ['день', 'дня', 'дней'])}.\nВаш малыш размером " \
                  f"с {children_content.text}.\n" \
                  f"Весит {int(children_content.weigh)}г.\n" \
                  f"И длиной {children_content.length}см."
        return message, f"{MEDIA_PATH}/{children_content.src}"
    return None, None


def declination(num, word):
    # declination(, ['неделю', 'недели', 'недель'])
    # declination(, ['день', 'дня', 'дней'])
    if len(str(num)) == 1:
        last_num = num
    else:
        last_num = int(num % 100)
        if last_num == 0 or last_num in [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]:
            return word[2]
        else:
            last_num = int(last_num % 10)
            if last_num == 1:
                return word[0]
            elif last_num in [2, 3, 4]:
                return word[1]
            else:
                return word[2]
    if last_num == 1:
        return word[0]
    elif last_num in [2, 3, 4]:
        return word[1]
    else:
        return word[2]


if __name__ == "__main__":
    print(get_user_name_from_vk_id(232551334))
