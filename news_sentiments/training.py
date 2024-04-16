import os
import numpy as np
import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification
import pandas as pd

# Parameters
MAX_LEN = 250
MODEL_PATH = 'sentiment_analysis_model'

file_path = 'all-data.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')
df_shuffled = data.sample(frac=1).reset_index(drop=True)

texts = df_shuffled['text_column'].tolist()
labels = np.array([0 if label == 0 else 1 if label ==
                  2 else 2 for label in df_shuffled['label_column'].values])

# Load BERT tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenize and pad the sequences
input_ids = tokenizer(texts, padding=True, truncation=True,
                      return_tensors="tf", max_length=MAX_LEN)['input_ids']

# Split data into training and test sets
train_data = input_ids[:-5000]
test_data = input_ids[-5000:]
train_labels = labels[:-5000]
test_labels = labels[-5000:]

# Load or train the model
if os.path.exists(MODEL_PATH):
    print("Loading saved model...")
    model = TFBertForSequenceClassification.from_pretrained(MODEL_PATH)
else:
    print("Training a new model...")
    # Load BERT model
    model = TFBertForSequenceClassification.from_pretrained(
        'bert-base-uncased')

    # Compile the model
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    for epoch in range(3):
        print(f"Epoch {epoch+1}/3")
        train_data_shuffled, train_labels_shuffled = tf.random.shuffle(train_data), tf.gather(
            train_labels, tf.random.shuffle(tf.range(tf.shape(train_data)[0])))

        model.fit(train_data_shuffled, train_labels_shuffled,
                  epochs=1, batch_size=8)

    # Save the trained model
    model.save_pretrained(MODEL_PATH)

# Evaluate on test data
loss, accuracy = model.evaluate(test_data, test_labels)
print(f"Test accuracy: {accuracy * 100:.2f}%")

# Interactive loop for predictions
while True:
    user_input = input(
        "Enter a sentence for sentiment analysis (or 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break

    encoded_input = tokenizer(user_input, padding=True, truncation=True,
                              return_tensors="tf", max_length=MAX_LEN)['input_ids']
    prediction = np.argmax(model.predict(encoded_input)[0])

    if prediction == 0:
        print("Sentiment: Negative")
    elif prediction == 1:
        print("Sentiment: Neutral")
    else:
        print("Sentiment: Positive")
