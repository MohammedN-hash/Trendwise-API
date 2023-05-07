import re
from transformers import pipeline

# load the emotion classifier
classifier = pipeline('text-classification', model='cardiffnlp/twitter-roberta-base-emotion', tokenizer='cardiffnlp/twitter-roberta-base-emotion')

def get_emotion(sentence):
    # check if input is a non-empty string
    if not isinstance(sentence, str) or not sentence.strip():
        return "Invalid input. Please provide a non-empty string."

    # remove all non-alphanumeric characters from the input sentence
    sentence = re.sub(r'[^\w\s,.!?]', '', sentence)

    # split the input sentence into a list of tokens
    tokens = sentence.split()

    # limit the length of the input sentence to 512 tokens
    if len(tokens) > 500:
        tokens = tokens[:500]
        sentence = " ".join(tokens)
        print("Input sentence exceeds maximum length of 512 tokens. Truncating to:", sentence)
    else:
        sentence = " ".join(tokens)

    # classify the emotion of the input sentence
    try:
        emotion = classifier(sentence)[0]['label']
        return emotion
    except Exception as e:
        print("Error:", e)
        return "Unable to classify emotion for input sentence."

# https://huggingface.co/j-hartmann/emotion-english-distilroberta-base?text=I%27ve+tried+both+docked+and+undocked+and+I+get+the+same+crash
