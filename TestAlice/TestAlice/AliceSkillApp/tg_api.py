from django.conf import settings
from telethon import TelegramClient
from telethon.tl.functions import messages
from telethon.tl.functions.contacts import ResolveUsernameRequest

import TestAlice.AliceSkillApp.redis_utils as redis_utils


api_id = settings.TG_API_ID
api_hash = settings.TG_API_HASH
tg_session_file = settings.TG_SESSION_FILE
client = TelegramClient(tg_session_file, api_id, api_hash)


async def async_get_channel_msgs(channel_name, limit=3, offset_id=0, offset_date=None, max_id=0, min_id=0):
    channel = redis_utils.get_channel(channel_name)
    if not channel:
        channel = await client(ResolveUsernameRequest(channel_name))
        redis_utils.save_channel(channel_name, channel)
    result = await client(messages.GetHistoryRequest(peer=channel, limit=limit, offset_id=offset_id,
                                                     offset_date=offset_date, add_offset=0, max_id=max_id,
                                                     min_id=min_id, hash=0))
    return result


def get_channel_msgs(channel_name, session_id, limit=3, offset_id=0, offset_date=None, max_id=0, min_id=0):
    with client:
        res = client.loop.run_until_complete(async_get_channel_msgs(channel_name, limit=limit, offset_date=offset_date,
                                                                    max_id=max_id, min_id=min_id, offset_id=offset_id))
        messages_str = [m.message for m in res.messages]
        messages_str = messages_str[-3:]
        messages_id = [m.id for m in res.messages]
        messages_id = messages_id[-3:]
        if messages_id:
            redis_utils.save_session_state(channel_name, session_id, messages_id)
        return messages_str


def get_next_messages(session_id):
    session = redis_utils.get_session_state(session_id)
    last_msg_id = session.get('msgs_id')[0]
    res = get_channel_msgs(session.get('channel_name'), session_id, min_id=last_msg_id, limit=0)
    return res if res else 'Далее постов нет'


def get_previous_messages(session_id):
    session = redis_utils.get_session_state(session_id)
    last_msg_id = session.get('msgs_id')[-1]
    res = get_channel_msgs(session.get('channel_name'), session_id, offset_id=last_msg_id)
    return res if res else 'Далее постов нет'


def get_messages_by_date(session_id, date):
    session = redis_utils.get_session_state(session_id)
    res = get_channel_msgs(session.get('channel_name'), session_id, offset_date=date)
    return res if res else 'Постов нет'
