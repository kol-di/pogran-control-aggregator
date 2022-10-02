import re
from cleantext import clean


def parse_locations(text):
    locations = []

    sent_pattern = re.compile(r"#(.*?)($|\.)", re.DOTALL)
    matches = re.finditer(sent_pattern, text)

    hashtag_pattern = re.compile(r"(?<=#)(.*?)(?=\s)")
    for match in matches:
        hashtags = re.findall(hashtag_pattern, clean(match.group(0), to_ascii=False, no_emoji=True))
        loc = {tag: 'y' for tag in hashtags}
        locations.append(loc)

    return locations


# with open('sample_text.txt') as f:
#     txt = f.read()
# print(parse_locations(txt))
