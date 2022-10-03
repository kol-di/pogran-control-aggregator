import re
from cleantext import clean
from string import ascii_lowercase


def parse_locations(text):
    locations = []

    sent_pattern = re.compile(r"#(.*?)($|\.)", re.DOTALL)
    matches = re.finditer(sent_pattern, text)

    hashtag_pattern = re.compile(r"(?<=#)(.*?)(?=\s)")
    for match in matches:
        hashtags = re.findall(hashtag_pattern, clean(match.group(0), to_ascii=False, no_emoji=True))
        loc = {tag: True for tag in hashtags}
        if 'отказ' not in hashtags:
            loc['отказ'] = False
        locations.append(loc)

    return locations


def get_msg_chunk(message):
    msg_chunk = []
    fields = (
        'id',
        'message',
        'date')

    serialized_msg = dict(filter(lambda el: el[0] in fields, message.to_dict().items()))
    try:
        msg_id, msg_txt, msg_date = [serialized_msg[key] for key in fields]
        location_tags = parse_locations(msg_txt)
        msg_chunk = [{
            '_id': str(msg_id) + loc_id,
            'date': msg_date,
            'refused': refused,
            'tags': tags}
            for loc_id, refused, tags in zip(
                ascii_lowercase[:len(location_tags)],
                map(lambda x: x['отказ'], location_tags),
                map(lambda x: (x, x.pop('отказ'))[0], location_tags))]
    except KeyError:
        pass

    return msg_chunk
