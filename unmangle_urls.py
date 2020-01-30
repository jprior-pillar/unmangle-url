#!/usr/bin/env python3

import sys
import re
from urllib.parse import urlparse, parse_qs, unquote


def extract_encoded_url(mangled_url):
    q = urlparse(mangled_url.strip())
    try:
        encoded_url = parse_qs(q.query)['u'][0]
    except KeyError:
        raise ValueError

    return encoded_url


def decode_url(encoded_url):
    encoded_url_with_percents = re.sub('-', '%', encoded_url)
    encoded_url_with_underscores = unquote(encoded_url_with_percents)
    decoded_url = re.sub('_', '/', encoded_url_with_underscores)
    return decoded_url


def main(mangled_urls):
    for mangled_url in mangled_urls:
        encoded_url = extract_encoded_url(mangled_url)
        decoded_url = decode_url(encoded_url)
        print(decoded_url)


if __name__ == '__main__':
    main(sys.argv[1:] or sys.stdin)
