import re
import unicodedata


def get_regex_match_group(regex, text):

    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
    try:
        return re.search(regex, text).group()
    except:
        return None