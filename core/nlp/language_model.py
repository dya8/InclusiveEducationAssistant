# core/nlp/language_model.py

class LanguageModel:
    def __init__(self, trie, ngram_model):
        self.trie = trie
        self.ngram = ngram_model

    def rank(self, context_words, prefix, top_k=3):
        scores = {}

        # CASE A: Typing word (prefix exists)
        if prefix:
            candidates = self.trie.get_words_with_prefix(prefix)

            for word, freq in candidates:
                context_score = 0

                if len(context_words) >= 2:
                    context_score += 0.7 * self.ngram.p_trigram(
                        context_words[-2], context_words[-1], word
                    )

                if len(context_words) >= 1:
                    context_score += 0.2 * self.ngram.p_bigram(
                        context_words[-1], word
                    )

                prefix_score = freq / self.ngram.total_words

                final_score = context_score + 0.1 * prefix_score
                scores[word] = final_score

        # CASE B: After space
        else:
            if len(context_words) >= 2:
                candidates = self.ngram.trigram.get(
                    (context_words[-2], context_words[-1]), {}
                ).keys()
            elif len(context_words) >= 1:
                candidates = self.ngram.bigram.get(
                    context_words[-1], {}
                ).keys()
            else:
                candidates = self.ngram.unigram.keys()

            for word in candidates:
                score = 0
                if len(context_words) >= 2:
                    score += 0.7 * self.ngram.p_trigram(
                        context_words[-2], context_words[-1], word
                    )
                if len(context_words) >= 1:
                    score += 0.2 * self.ngram.p_bigram(
                        context_words[-1], word
                    )
                score += 0.1 * self.ngram.p_unigram(word)

                scores[word] = score

        return sorted(scores, key=scores.get, reverse=True)[:top_k]