from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf


def predict_sentiment(text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = TFBertForSequenceClassification.from_pretrained(
        'bert-base-uncased')
    input_ids = tokenizer(text, padding=True, truncation=True,
                          return_tensors="tf", max_length=250)['input_ids']
    logits = model(input_ids)[0]  # Get the logits from the model
    # Convert logits to probabilities
    probabilities = tf.nn.softmax(logits, axis=-1)
    # Get the predicted class index
    predicted_class = tf.argmax(probabilities, axis=-1).numpy()[0]
    sentiment_labels = ['Negative', 'Neutral', 'Positive']
    predicted_sentiment = sentiment_labels[predicted_class]
    return predicted_sentiment
