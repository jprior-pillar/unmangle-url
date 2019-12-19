#!/usr/bin/env python3

import sys
import re


def extract_encoded_url(mangled_url):
    m = re.search(r'\bu=(?P<encoded_url>[^&]*)', mangled_url.strip())
    try:
        encoded_url = m.group('encoded_url')
    except AttributeError:
        raise ValueError

    return encoded_url


def decode_chunk(chunk):
    encoded_character_pattern = r'([-](?P<character_code>[0-9A-F]{2}))'
    m = re.fullmatch(encoded_character_pattern, chunk)
    try:
        decoded_chunk = chr(int(m.group('character_code'), 0x10))
    except AttributeError:
        decoded_chunk = chunk

    return decoded_chunk


def decode_url(encoded_url):
    encoded_character_pattern = re.compile(r'([-][0-9A-F]{2})')
    encoded_url_with_slashes = re.sub('_', '/', encoded_url)
    encoded_chunks = re.split(encoded_character_pattern, encoded_url_with_slashes)
    decoded_chunks = map(decode_chunk, encoded_chunks)
    decoded_url = ''.join(decoded_chunks)

    return decoded_url


def main(mangled_urls):
    for mangled_url in mangled_urls:
        encoded_url = extract_encoded_url(mangled_url)
        decoded_url = decode_url(encoded_url)
        print(decoded_url)


if __name__ == '__main__':
    main(sys.stdin)
