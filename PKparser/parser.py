import re
from cleantext import clean
from string import ascii_lowercase


def parse_tags(text):
    locations = []

    sent_pattern = re.compile(r"#(.*?)($|\.)", re.DOTALL)
    matches = re.finditer(sent_pattern, text)

    hashtag_pattern = re.compile(r"(?<=#)(.*?)(?=\s)")
    for match in matches:
        hashtags = re.findall(hashtag_pattern, clean(match.group(0), to_ascii=False, no_emoji=True))
        refuse_and_locs = ('отказ' in hashtags, hashtags)
        locations.append(refuse_and_locs)

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
        location_tags = parse_tags(msg_txt)
        msg_chunk = [{
            '_id': str(msg_id) + loc_id,
            'date': msg_date,
            'refused': refused,
            'tags': tags}
            for loc_id, refused, tags in zip(
                ascii_lowercase[:len(location_tags)],
                map(lambda x: x[0], location_tags),
                map(lambda x: x[1], location_tags))]
    except KeyError:
        pass

    return msg_chunk
