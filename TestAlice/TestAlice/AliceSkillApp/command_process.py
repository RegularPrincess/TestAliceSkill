from datetime import datetime, timedelta
import TestAlice.AliceSkillApp.redis_utils as redis_utils
from telethon.errors.rpcerrorlist import UsernameInvalidError, UsernameNotOccupiedError

from TestAlice.AliceSkillApp import tg_api


def process_command(command_str, entities, session_id):
    if not redis_utils.is_new_session(session_id):
        if _next_command(command_str):
            return tg_api.get_next_messages(session_id)
        elif _back_command(command_str):
            return tg_api.get_previous_messages(session_id)
        elif _date_command(entities):
            date = _extract_date(entities)
            return tg_api.get_messages_by_date(session_id, date)
    try:
        answer = tg_api.get_channel_msgs(command_str, session_id)
    except (UsernameInvalidError, UsernameNotOccupiedError):
        answer = 'Канала "%s" не существует.' % command_str
    return answer


def _has_occurrence(string, sub_strs):
    string = string.lower()
    for n in sub_strs:
        if n in string:
            return True
    return False


def _next_command(command):
    return _has_occurrence(command, sub_strs=('next', 'дальше'))


def _back_command(command):
    return _has_occurrence(command, sub_strs=('back', 'назад'))


def _date_command(entities):
    for entity in entities:
        if entity['type'] == 'YANDEX.DATETIME':
            return True
    return False


def _extract_date(entities):
    date_entity = None
    for entity in entities:
        if entity['type'] == 'YANDEX.DATETIME':
            date_entity = entity
    days = date_entity['value']['day']
    date = datetime.today() + timedelta(days=days)
    return date
