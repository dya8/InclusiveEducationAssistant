# core/nlp/predictor.py

from .tokenizer import extract_context_and_prefix
from .language_model import LanguageModel
from .trie import Trie
from .ngram_model import NGramModel


class Predictor:
    def __init__(self, model_path):
        self.ngram = NGramModel.load(model_path)

        self.trie = Trie()
        for word, freq in self.ngram.unigram.items():
            self.trie.insert(word, freq)

        self.language_model = LanguageModel(self.trie, self.ngram)

    def get_suggestions(self, text, top_k=3):
        context, prefix = extract_context_and_prefix(text)
        return self.language_model.rank(context, prefix, top_k=top_k)