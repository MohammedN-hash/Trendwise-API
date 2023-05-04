
from transformers import pipeline
import re

classifier = pipeline("text-classification",
                      model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)


def get_emotion(sentence):
    # check if input is a non-empty string
    if not isinstance(sentence, str) or not sentence.strip():
        return "Invalid input. Please provide a non-empty string."

    # remove all non-alphanumeric characters from the input sentence
    sentence = re.sub(r'[^\w\s]', '', sentence)

    # limit the length of the input sentence to 512 tokens
    sentence = " ".join(sentence.split()[:512])

    print(sentence)

    # check if sentence length is less than or equal to 512 tokens
    if len(sentence.split()) <= 512:
        # classify the emotion of the input sentence
        emotion = classifier(sentence)[0]['label']
        print(emotion)
        return emotion
    else:
        return "Input sentence exceeds maximum length of 512 tokens."

# https://huggingface.co/j-hartmann/emotion-english-distilroberta-base?text=I%27ve+tried+both+docked+and+undocked+and+I+get+the+same+crash
