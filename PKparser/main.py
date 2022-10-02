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

from parser import parse_locations


logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    filename='handler.log',
    level=logging.WARNING)

config_path = pathlib.Path(__file__).parent.absolute() / "config.ini"
config = configparser.ConfigParser()
config.read(config_path)

API_ID = config['Telegram']['api_id']
API_HASH = config['Telegram']['api_hash']
USERNAME = config['Telegram']['username']
CHANNEL_URL = config['Telegram']['channel_url']

client = TelegramClient(USERNAME, API_ID, API_HASH)
client.start()


async def dump_all_messages(channel):
    """Creates JSON with all channel messages"""
    limit_msg = 100  # message limit per api call
    offset_min = 0

    all_messages = []
    total_count_limit = 0  # change to get only a portion of messages

    fields = (
        'id',
        'message',
        'date'
    )

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
            all_messages.append(dict(
                filter(lambda el: el[0] in fields, message.to_dict().items())))

        offset_min += limit_msg
        total_messages = len(all_messages)

        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    with open('channel_messages.json', 'w', encoding='utf8') as outfile:
        json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


async def main(argv):
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

    channel_peer = await client.get_entity(CHANNEL_URL)
    if arg_rewrite == 'y':
        await dump_all_messages(channel_peer)
    return channel_peer


channel_peer = client.loop.run_until_complete(main(sys.argv))


@client.on(events.NewMessage(chats=[channel_peer]))
async def handler(event):
    text = event.raw_text
    print('ye', parse_locations(text))


print(f'Is bot? {client.is_bot()}')
print(f'Is authorized? {client.is_user_authorized()}')
print(f'I am {client.get_me()}')
client.run_until_disconnected()
