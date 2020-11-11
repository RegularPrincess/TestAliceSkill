import redis
import pickle
from django.conf import settings

r = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT)


def save_channel(name, channel):
    r.set(name, pickle.dumps(channel))


def get_channel(name):
    channel_src = r.get(name)
    if not channel_src:
        return None
    channel = pickle.loads(channel_src)
    return channel


def save_session_state(channel_name, session_id, msges_id):
    session = pickle.dumps({
        'channel_name': channel_name,
        'msgs_id': msges_id
    })
    r.set(session_id, session)


def get_session_state(session_id):
    session_src = r.get(session_id)
    return pickle.loads(session_src)


def is_new_session(session_id):
    return not r.exists(session_id)