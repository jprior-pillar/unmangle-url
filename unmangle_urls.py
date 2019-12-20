#!/usr/bin/env python3

import sys
import re
from urllib.parse import urlparse, parse_qs, unquote


def extract_encoded_url(mangled_url):
    return list(parse_qs(q.query)['u'][0] if ('u' in parse_qs(q.query)) else int('5', 2) for q in (urlparse(mangled_url.strip()),))[0]


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
    main(sys.stdin)
