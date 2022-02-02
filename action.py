from keyboard import settings_keyboard, main_keyboard, born_keyboard
from function import get_user_name_from_vk_id, get_users_due_date, calculate_week_and_day, get_user, \
    set_sub, write_msg, about_children, about_mom_children, next_post
from settings import LIFE_SET_KEY
from bd import r, next_collection
from mongo_function import find_document


def settings_keys(vk, id_):
    write_msg(vk, id_, "Настройки", settings_keyboard)


def about_child(vk, id_):
    about_mom_children(vk, id_, "children")


def about_mom(vk, id_):
    about_mom_children(vk, id_, "mama")


def interested_fact(vk, id_):
    due_date = get_users_due_date(vk, id_)
    if due_date:
        days, weeks = calculate_week_and_day(due_date)
        write_msg(vk, id_, "Интересный факт")


def recom_today(vk, id_):
    due_date = get_users_due_date(vk, id_)
    if due_date:
        days, weeks = calculate_week_and_day(due_date)
        write_msg(vk, id_, "Рекомендации на сегодня")


def go_to_main(vk, id_):
    message, src = about_children(vk, id_)
    if not message:
        write_msg(vk, id_, "На главную", main_keyboard)
    else:
        write_msg(vk, id_, message, main_keyboard, img_path=src)


def set_born_day(vk, id_):
    write_msg(vk, id_,
              f"{get_user_name_from_vk_id(id_)} ты знаешь дату родов ?", born_keyboard)


def born(vk, id_):
    r.setex(str(id_), LIFE_SET_KEY, 'born')
    write_msg(vk, id_, '💭Введи дату родов в формате "дд.мм.гггг"')


def blood(vk, id_):
    r.setex(str(id_), LIFE_SET_KEY, 'blood')
    write_msg(vk, id_, '💭Напиши дату ласт месяков в формате "дд.мм.гггг" Мы типо рассчитаем акушерским методом '
                       'и примерно напишем когда у тебя будут роды')


def subscribe(vk, id_):
    model = get_user(vk, id_)
    if model:
        set_sub(id_, True)
        write_msg(vk, id_, "Спасибо, Вы подписались на рассылку.")
    print(f"{id_} subscribe")


def unsubscribe(vk, id_):
    model = get_user(vk, id_)
    if model:
        set_sub(id_, False)
        write_msg(vk, id_, "Вы отписались от рассылки.")
    print(f"{id_} unsubscribe")


def next_post_mama(vk, id_):
    next_post(vk, id_, "mama")


def next_post_children(vk, id_):
    next_post(vk, id_, "children")
