import re
from cleantext import clean
from string import ascii_lowercase


def parse_tags(text):
    tags = []

    transport_tags = [
        'авто',
        'жд',
        'авиа',
        'самолет',
        'автобус',
        'аэропорт'
    ]
    refuse_tag = 'отказ'

    sent_pattern = re.compile(r"#(.*?)($|\.)", re.DOTALL)
    matches = re.finditer(sent_pattern, text)

    hashtag_pattern = re.compile(r"(?<=#)(.*?)(?=\s)")
    for match in matches:
        hashtags = re.findall(hashtag_pattern, clean(match.group(0), to_ascii=False, no_emoji=True))
        if refuse := refuse_tag in hashtags:
            hashtags.remove(refuse_tag)
        transport = [var for var in hashtags if var in transport_tags]
        for var in transport:
            hashtags.remove(var)
        tag_tuple = (refuse, transport, hashtags)
        tags.append(tag_tuple)

    return tags


def get_msg_chunk(message):
    msg_chunk = []
    fields = (
        'id',
        'message',
        'date')

    serialized_msg = dict(filter(lambda el: el[0] in fields, message.to_dict().items()))
    try:
        msg_id, msg_txt, msg_date = [serialized_msg[key] for key in fields]
        tags = parse_tags(msg_txt)
        msg_chunk = [{
            '_id': str(msg_id) + loc_id,
            'date': msg_date,
            'refused': refused,
            'transport': transport,
            'locations': locations}
            for loc_id, refused, transport, locations in zip(
                ascii_lowercase[:len(tags)],
                map(lambda x: x[0], tags),
                map(lambda x: x[1], tags),
                map(lambda x: x[2], tags))]
    except KeyError:
        pass

    return msg_chunk
