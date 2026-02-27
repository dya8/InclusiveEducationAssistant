# experiments/train_ngram.py

import os
import nltk
from nltk.corpus import brown
from core.nlp.ngram_model import NGramModel

# Download once
nltk.download("brown")

# Prepare sentences
sentences = brown.sents()
sentences = [
    [word.lower() for word in sent if word.isalpha()]
    for sent in sentences
]

# Train model
model = NGramModel()
model.train(sentences)

# Ensure models directory exists
os.makedirs("assets/models", exist_ok=True)

# Save model
model.save("assets/models/ngram_model.pkl")

print("Model trained and saved successfully.")