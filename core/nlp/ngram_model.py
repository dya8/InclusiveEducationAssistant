# core/nlp/ngram_model.py

from collections import Counter, defaultdict
import pickle

class NGramModel:
    def __init__(self):
        self.unigram = Counter()
        self.bigram = defaultdict(Counter)
        self.trigram = defaultdict(Counter)
        self.bigram_totals = {}
        self.trigram_totals = {}
        self.total_words = 0
        self.V = 0

    def train(self, sentences):
        for sent in sentences:
            for i in range(len(sent)):
                self.unigram[sent[i]] += 1

                if i >= 1:
                    self.bigram[sent[i-1]][sent[i]] += 1

                if i >= 2:
                    self.trigram[(sent[i-2], sent[i-1])][sent[i]] += 1

        self.total_words = sum(self.unigram.values())
        self.V = len(self.unigram)

        # Precompute totals
        for w1 in self.bigram:
            self.bigram_totals[w1] = sum(self.bigram[w1].values())

        for context in self.trigram:
            self.trigram_totals[context] = sum(self.trigram[context].values())

    def p_unigram(self, w):
        return self.unigram[w] / self.total_words if self.total_words else 0

    def p_bigram(self, w1, w2):
        total = self.bigram_totals.get(w1, 0)
        return (self.bigram[w1][w2] + 1) / (total + self.V)

    def p_trigram(self, w1, w2, w3):
        total = self.trigram_totals.get((w1, w2), 0)
        return (self.trigram[(w1, w2)][w3] + 1) / (total + self.V)

    def save(self, path):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path):
        with open(path, "rb") as f:
            return pickle.load(f)