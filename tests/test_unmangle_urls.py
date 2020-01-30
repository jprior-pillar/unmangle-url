import pytest

from unmangle_urls import extract_encoded_url, decode_url, main


mangled_url__encoded_urls = (
    (
        'https://foo.com/v2/url?u=https-3A__www.youtube.com_&d=D&e=',
        'https-3A__www.youtube.com_',
    ),
    (
        'https://bar.com/v3/url?u=http-3A__colug.net_&v=V',
        'http-3A__colug.net_',
    ),
    (
        'https://bar.com/v3/url?u=http-3A__colug.net_',
        'http-3A__colug.net_',
    ),
    (
        '  https://bar.com/v3/url?u=http-3A__colug.net_ \n',
        'http-3A__colug.net_',
    ),
)
@pytest.mark.parametrize('mangled_url, encoded_url', mangled_url__encoded_urls)
def test_extract_encoded_url(mangled_url, encoded_url):
    expected_url = encoded_url
    actual = extract_encoded_url(mangled_url)
    assert expected_url == actual


def test_extract_encoded_url__without_encoded_url__raises_exception():
    mangled_url = 'https://foo.com/v2/url?v=https-3A__www.youtube.com_&d=D&e='
    with pytest.raises(ValueError):
        extract_encoded_url(mangled_url)


encoded_url__decoded_urls = (
    ('https-3A__www.youtube.com_w-3Fv-3Dv', 'https://www.youtube.com/w?v=v'),
    ('http-3A__colug.net_', 'http://colug.net/'),
)
@pytest.mark.parametrize('encoded_url, decoded_url', encoded_url__decoded_urls)
def test_decode_url(encoded_url, decoded_url):
    expected_url = decoded_url
    actual_url = decode_url(encoded_url)
    assert expected_url == actual_url


mangled_url__decoded_urls = (
    (
        'https://foo.com/v2/url?u=https-3A__www.youtube.com_&d=D&e=',
        'https://www.youtube.com/',
    ),
    (
        'https://bar.com/v3/url?u=http-3A__colug.net_&v=V',
        'http://colug.net/',
    ),
    (
        'https://bar.com/v3/url?u=http-3A__colug.net_',
        'http://colug.net/',
    ),
)
@pytest.mark.parametrize('mangled_url, decoded_url', mangled_url__decoded_urls)
def test_extract_url(mangled_url, decoded_url):
    # mangled_url = 'https://foo.com/v2/url?u=https-3A__www.youtube.com_&d=D&e='
    # decoded_url = 'https://www.youtube.com/'
    expected_url = decoded_url
    encoded_url = extract_encoded_url(mangled_url)
    actual_url = decode_url(encoded_url)
    assert expected_url == actual_url


test_data = (
    (
        ['unmangle_urls.py'],
        (
            ( 'https://foo.com/v2/url?u=https-3A__www.youtube.com_&d=D&e=\n' ),
            ( 'https://bar.com/v3/url?u=http-3A__colug.net_\n' ),
        ),
        (
            'https://www.youtube.com/\n'
            'http://colug.net/\n'
        ),
    ),
    (
        [
            'unmangle_urls.py',
            'https://bar.com/v3/url?u=http-3A__colug.net_',
        ],
        (
            ( 'https://foo.com/v2/url?u=https-3A__www.youtube.com_&d=D&e=\n' ),
        ),
        (
            'http://colug.net/\n'
        ),
    ),
)
@pytest.mark.parametrize(
    'command_line_arguments, lines, expected_output', test_data)
def test_main(command_line_arguments, lines, expected_output, capsys):
    main(command_line_arguments[1:] or lines)
    captured = capsys.readouterr()
    actual_output = captured.out
    assert expected_output == actual_output
