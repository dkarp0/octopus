from collections import Counter

import page_parser

parser = page_parser.Parser


def test_parser_empty():
    assert (parser.parse('') == list())


def test_parser_single_word():
    assert (parser.parse('hello') == [('hello', 1)])


def test_parser_multi_words():
    assert (Counter(parser.parse('hello world')) == Counter([('hello', 1), ('world', 1)]))


def test_parser_multi_words_count():
    assert (Counter(parser.parse('hello hello')) == Counter([('hello', 2)]))
    assert (Counter(parser.parse('hello hello world world')) == Counter([('hello', 2), ('world', 2)]))


def test_parser_remove_non_visible():
    html = """
    <script>we don't want this visible</script>
    hello world <style>or this</style>
    """
    assert (Counter(parser.parse(html)) == Counter([('hello', 1), ('world', 1)]))


def test_parser_remove_non_noun():
    html = """
    I say hello in worlds
    """
    assert (Counter(parser.parse(html)) == Counter([('say', 1), ('hello', 1), ('worlds', 1)]))
