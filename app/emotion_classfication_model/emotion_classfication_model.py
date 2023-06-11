import re
import requests

API_URL = "https://api-inference.huggingface.co/models/aleryanimohammed/M.A-emotion-classficatio-model-Bert"
headers = {"Authorization": "Bearer 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"}
emotion_mapping = {
    "LABEL_0": "neutral",
    "LABEL_1": "happiness",
    "LABEL_2": "sadness",
    "LABEL_3": "anger",
    "LABEL_4": "surprise",
    "LABEL_5": "fear",
    "LABEL_6": "disgust",
    "LABEL_7": "enthusiasm"
}
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def get_predicted_emotion(output):
    emotions = output[0]  # Get the inner list of emotions
    highest_emotion = max(emotions, key=lambda x: x['score'])
    predicted_emotion_label = highest_emotion['label']
    
    return predicted_emotion_label

def get_emotion(sentence):
    # check if input is a non-empty string
    if not isinstance(sentence, str) or not sentence.strip():
        return "Invalid input. Please provide a non-empty string."

    # remove all non-alphanumeric characters from the input sentence
    sentence = re.sub(r'[^\w\s,.!?]', '', sentence)

    # split the input sentence into a list of tokens
    tokens = sentence.split()

    # limit the length of the input sentence to 512 tokens
    if len(tokens) > 512:
        tokens = tokens[:512]
        sentence = " ".join(tokens)
        print("Input sentence exceeds maximum length of 512 tokens. Truncating to:", sentence)
    else:
        sentence = " ".join(tokens)

    # classify the emotion of the input sentence
    try:
        output = query({
            "inputs": sentence
        })
        predicted_emotion = get_predicted_emotion(output)
        return predicted_emotion
    except Exception as e:
        print("Error:", e)
        return "Unable to classify emotion for input sentence."



# #  Load the pre-trained model and tokenizer from the local folder
# model_path = "distilbert_base_uncased_with_weight"

# # Load the configuration
# config = transformers.AutoConfig.from_pretrained('distilbert_base_uncased_with_weight/config.json')

# # Load the tokenizer
# tokenizer = transformers.AutoTokenizer.from_pretrained('distilbert_base_uncased_with_weight')

# # Load the model
# model = transformers.AutoModel.from_pretrained('distilbert_base_uncased_with_weight/pytorch_model.bin', config=config)
# emotion_mapping = {
#     0: "neutral",
#     1: "happiness",
#     2: "sadness",
#     3: "anger",
#     4: "surprise",
#     5: "fear",
#     6: "disgust",
#     7: "enthusiasm"
# }
# def get_emotion(input_text):
#     # Tokenize the input text
#     encoded_input = tokenizer.encode_plus(input_text, padding="max_length", truncation=True, max_length=128, return_tensors="pt")
    
#     # Make a prediction
#     with torch.no_grad():
#         logits = model(**encoded_input).logits
    
#     # Decode the output
#     predicted_class = torch.argmax(logits, dim=1).item()
#     predicted_label = emotion_mapping[predicted_class]

#     return predicted_label














# load the emotion classifier from huugingface opensource lib
# classifier = pipeline('text-classification', model='cardiffnlp/twitter-roberta-base-emotion', tokenizer='cardiffnlp/twitter-roberta-base-emotion')
# classifier = pipeline('text-classification', model="pipeline_distilbert", tokenizer="pipeline_distilbert")

# def get_emotion(sentence):
#     # check if input is a non-empty string
#     if not isinstance(sentence, str) or not sentence.strip():
#         return "Invalid input. Please provide a non-empty string."

#     # remove all non-alphanumeric characters from the input sentence
#     sentence = re.sub(r'[^\w\s,.!?]', '', sentence)

#     # split the input sentence into a list of tokens
#     tokens = sentence.split()

#     # limit the length of the input sentence to 512 tokens
#     if len(tokens) > 500:
#         tokens = tokens[:500]
#         sentence = " ".join(tokens)
#         print("Input sentence exceeds maximum length of 512 tokens. Truncating to:", sentence)
#     else:
#         sentence = " ".join(tokens)

#     # classify the emotion of the input sentence
#     try:
#         emotion = classifier(sentence)[0]['label']
#         return emotion
#     except Exception as e:
#         print("Error:", e)
#         return "Unable to classify emotion for input sentence."

# # https://huggingface.co/j-hartmann/emotion-english-distilroberta-base?text=I%27ve+tried+both+docked+and+undocked+and+I+get+the+same+crash
