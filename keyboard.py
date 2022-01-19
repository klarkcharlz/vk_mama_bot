from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from settings import CHAT_URL

# Главная Клавиатура
main_keyboard_settings = {'one_time': False,
                          'inline': False}
main_keyboard = VkKeyboard(**main_keyboard_settings)

main_keyboard.add_callback_button(label='Узнать чо ща с малышом🤰',
                                  color=VkKeyboardColor.POSITIVE,
                                  payload={"type": "about_child"})
main_keyboard.add_line()
main_keyboard.add_callback_button(label='Узнать что ща с твоим организмом🤷',
                                  color=VkKeyboardColor.POSITIVE,
                                  payload={"type": "about_mom"})
main_keyboard.add_line()
main_keyboard.add_callback_button(label='Интересный факт🤓',
                                  color=VkKeyboardColor.POSITIVE,
                                  payload={"type": "interested_fact"})
main_keyboard.add_line()
main_keyboard.add_callback_button(label='Рекомендация на сегодня🕑',
                                  color=VkKeyboardColor.POSITIVE,
                                  payload={"type": "recom_today"})
main_keyboard.add_line()
main_keyboard.add_callback_button(label='Настройки',
                                  color=VkKeyboardColor.PRIMARY,
                                  payload={"type": "settings"})
main_keyboard.add_callback_button(label='Чат с бабами',
                                  color=VkKeyboardColor.SECONDARY,
                                  payload={"type": "open_link", "link": CHAT_URL})

# inline нкопка для показа главной клавиатуры
start_button_settings = {'one_time': False,
                         'inline': True}
start_button = VkKeyboard(**start_button_settings)
start_button.add_button(label='Начать',
                        color=VkKeyboardColor.PRIMARY)

# settings клавиатура
settings_keyboard_settings = {'one_time': False,
                              'inline': False}
settings_keyboard = VkKeyboard(**settings_keyboard_settings)

settings_keyboard.add_callback_button(label='На главную',
                                      color=VkKeyboardColor.SECONDARY,
                                      payload={"type": "go_to_main"})
settings_keyboard.add_line()
settings_keyboard.add_callback_button(label='Подписаться',
                                      color=VkKeyboardColor.POSITIVE,
                                      payload={"type": "subscribe"})
settings_keyboard.add_line()
settings_keyboard.add_callback_button(label='Изменить дату родов',
                                      color=VkKeyboardColor.PRIMARY,
                                      payload={"type": "set_born_day"})
settings_keyboard.add_line()
settings_keyboard.add_callback_button(label='Отписаться',
                                      color=VkKeyboardColor.SECONDARY,
                                      payload={"type": "unsubscribe"})


# inline клавиатура для установки даты
born_keyboard_settings = {'one_time': False,
                          'inline': True}
born_keyboard = VkKeyboard(**born_keyboard_settings)
born_keyboard.add_callback_button(label='Да, знаю!',
                                  color=VkKeyboardColor.PRIMARY,
                                  payload={"type": "born"})
born_keyboard.add_callback_button(label='Нет, но хочу знать!',
                                  color=VkKeyboardColor.PRIMARY,
                                  payload={"type": "blood"})
