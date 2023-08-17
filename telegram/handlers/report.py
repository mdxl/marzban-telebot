import datetime

from app import logger
from app.telegram import bot
from telebot.apihelper import ApiTelegramException
from datetime import datetime
from app.telegram.utils.keyboard import BotKeyboard
from app.utils.system import readable_size
from config import TELEGRAM_ADMINS_ID, TELEGRAM_LOGGER_CHANNEL_ID
from telebot.formatting import escape_html


def report(message: str, parse_mode="html", keyboard=None):
    if bot and TELEGRAM_ADMINS_ID:
        try:
            if TELEGRAM_LOGGER_CHANNEL_ID:
                bot.send_message(TELEGRAM_LOGGER_CHANNEL_ID, message, parse_mode=parse_mode)
            else:
                for admin in TELEGRAM_ADMINS_ID:
                    bot.send_message(admin, message, parse_mode=parse_mode, reply_markup=keyboard)
        except ApiTelegramException as e:
            logger.error(e)


def report_new_user(user_id: int, username: str, by: str, expire_date: int, usage: str, proxies: list):
    text = '''\
🆕 <b>#Создан</b>
➖➖➖➖➖➖➖➖➖
<b>Имя пользователя :</b> <code>{username}</code>
<b>Лимит трафика :</b> <code>{usage}</code>
<b>Срок действия :</b> <code>{expire_date}</code>
<b>Прокси  :</b> <code>{proxies}</code>
➖➖➖➖➖➖➖➖➖
<b>By :</b> <b>#{by}</b>'''.format(
        by=escape_html(by),
        username=escape_html(username),
        usage=readable_size(usage) if usage else "Unlimited",
        expire_date=datetime.fromtimestamp(expire_date).strftime("%H:%M:%S %Y-%m-%d") if expire_date else "Never",
        proxies="" if not proxies else ", ".join([escape_html(proxy.type) for proxy in proxies])
    )

    return report(
        text,
        keyboard=BotKeyboard.user_menu({
            'username': username,
            'id': user_id,
            'status': 'active'
        }, with_back=False)
    )


def report_user_modification(username: str, expire_date: int, usage: str, proxies: list, by: str):
    text = '''\
✏️ <b>#Изменен</b>
➖➖➖➖➖➖➖➖➖
<b>Имя пользователя :</b> <code>{username}</code>
<b>Лимит трафика :</b> <code>{usage}</code>
<b>Срок действия :</b> <code>{expire_date}</code>
<b>Протоколы :</b> <code>{protocols}</code>
➖➖➖➖➖➖➖➖➖
<b>By :</b> <b>#{by}</b>\
    '''.format(
        by=escape_html(by),
        username=escape_html(username),
        usage=readable_size(usage) if usage else "Unlimited",
        expire_date=datetime.fromtimestamp(expire_date).strftime("%H:%M:%S %Y-%m-%d") if expire_date else "Never",
        protocols=', '.join([p.type for p in proxies])
    )

    return report(text, keyboard=BotKeyboard.user_menu({
        'username': username,
        'status': 'active'
    }, with_back=False))


def report_user_deletion(username: str, by: str):
    text = '''\
🗑 <b>#Удален</b>
➖➖➖➖➖➖➖➖➖
<b>Имя пользователя</b> : <code>{username}</code>
➖➖➖➖➖➖➖➖➖
<b>От</b> : <b>#{by}</b>\
    '''.format(
        by=escape_html(by),
        username=escape_html(username)
    )
    return report(text)


def report_status_change(username: str, status: str):
    _status = {
        'active': '✅ <b>#Активирован</b>',
        'disabled': '❌ <b>#Отключен</b>',
        'limited': '🪫 <b>#Ограничен</b>',
        'expired': '🕔 <b>#Истек</b>'
    }
    text = '''\
{status}
➖➖➖➖➖➖➖➖➖
<b>Username</b> : <code>{username}</code>\
    '''.format(
        username=escape_html(username),
        status=_status[status]
    )
    return report(text)
