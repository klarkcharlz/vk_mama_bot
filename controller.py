from action import (settings_keys,
                    about_child,
                    about_mom,
                    interested_fact,
                    go_to_main,
                    set_born_day,
                    born,
                    blood,
                    recom_today,
                    subscribe,
                    unsubscribe,
                    next_post_mama,
                    next_post_children
                    )

ACTION = {
    "about_child": about_child,
    "about_mom": about_mom,
    "interested_fact": interested_fact,
    "recom_today": recom_today,
    "settings": settings_keys,
    "go_to_main": go_to_main,
    "subscribe": subscribe,
    "set_born_day": set_born_day,
    "unsubscribe": unsubscribe,
    "born": born,
    "blood": blood,
    "mama_next_post": next_post_mama,
    "children_next_post": next_post_children
}

MES_COM = {
    'узнать чо ща с малышом': about_child,
    'узнать что ща с твоим организмом': about_mom,
    'интересный факт': interested_fact,
    'рекомендация на сегодня': recom_today,
    'настройки': settings_keys,
    'на главную': go_to_main,
    'подписаться': subscribe,
    'изменить дату родов': set_born_day,
    'отписаться': unsubscribe,
    'да, знаю': born,
    'нет, но хочу знать': blood,
    "далее о маме": next_post_mama,
    "далее о ребенке": next_post_children
}
