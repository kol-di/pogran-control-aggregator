import configparser
import json
import pathlib
import logging
import sys
import getopt

from datetime import datetime

from telethon.sync import TelegramClient
from telethon import events
from telethon.tl.functions.messages import GetHistoryRequest

from parser import get_msg_chunk

from db_locations import initialize_db

# enable logging
logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    filename='handler.log',
    level=logging.WARNING)

# read sensitive configs
config_path = pathlib.Path(__file__).parent.absolute() / "config.ini"
config = configparser.ConfigParser()
config.read(config_path)

API_ID = config['Telegram']['api_id']
API_HASH = config['Telegram']['api_hash']
USERNAME = config['Telegram']['username']
CHANNEL_URL = config['Telegram']['channel_url']

client = TelegramClient(USERNAME, API_ID, API_HASH)
client.start()


async def _dump_all_messages(channel, collection):
    """Creates JSON with all channel messages"""
    limit_msg = 100  # message limit per api call
    offset_min = 0

    all_messages = []
    total_count_limit = 0  # change to get only a portion of messages

    class DateTimeEncoder(json.JSONEncoder):
        """JSON date serializer"""
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return json.JSONEncoder.default(self, o)

    while True:
        print(offset_min)
        history = await client(GetHistoryRequest(
            peer=channel,
            limit=limit_msg,
            offset_id=offset_min + limit_msg,
            min_id=offset_min,
            offset_date=None,
            add_offset=0,
            max_id=offset_min + limit_msg,
            hash=0))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages += get_msg_chunk(message)

        offset_min += limit_msg
        total_messages = len(all_messages)

        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    collection.insert_many(all_messages)

    with open('channel_messages.json', 'w', encoding='utf8') as outfile:
        json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


def _pars_args(argv):
    arg_rewrite = ''
    arg_help = "{0} -r <rewrite>".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hr:", ["help", "rewrite="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-r", "--rewrite"):
            arg_rewrite = arg
            assert arg_rewrite in ('y', 'n'), "Specify either y or n"

    return arg_rewrite


async def main(argv):
    channel_peer = await client.get_entity(CHANNEL_URL)

    db = initialize_db()

    arg_rewrite = _pars_args(argv)
    if arg_rewrite == 'y':
        await _dump_all_messages(channel_peer, db['locations'])

    return channel_peer, db


channel_peer, db = client.loop.run_until_complete(main(sys.argv))


@client.on(events.NewMessage(chats=[channel_peer]))
async def handler(event):
    text = event.message
    msg_chunk = get_msg_chunk(text)
    db['locations'].insert_many(msg_chunk)


print(f'Is bot? {client.is_bot()}')
print(f'Is authorized? {client.is_user_authorized()}')

client.run_until_disconnected()
db.close()
