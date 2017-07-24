import nltk
from bs4 import BeautifulSoup


class Parser:
    @staticmethod
    def parse(html):
        soup = BeautifulSoup(html, 'html.parser')
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        tokenised = Parser._tokenise(soup.get_text())
        cleaned = Parser._remove_prepositions_and_articles(tokenised)
        return Parser._get_frequency_dist(cleaned)

    @staticmethod
    def _tokenise(s):
        return nltk.word_tokenize(s)

    @staticmethod
    def _remove_prepositions_and_articles(s):
        return [k[0] for k in nltk.pos_tag(s, tagset='universal') if k[1] in ['NOUN', 'VERB']]

    @staticmethod
    def _get_frequency_dist(tokenised):
        return nltk.FreqDist(tokenised).most_common()
