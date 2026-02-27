from core.nlp.predictor import Predictor

predictor = Predictor("assets/models/ngram_model.pkl")

while True:
    text = input("Type sentence: ")
    suggestions = predictor.get_suggestions(text)
    print("Suggestions:", suggestions)