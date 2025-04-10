# -*- coding: utf-8 -*-
"""hate_speech.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YmOy4w8irAjEQZjNMQUA5UKm71F0kTfc

Importing the pandas 😀
"""

!pip install pandas numpy scikit-learn nltk tensorflow keras

"""Importing Data set and code for train the model"""

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. Load data
df = pd.read_csv("Hate_speechdata.csv", encoding='latin1')  # replace with actual path

# 2. Keep only relevant columns
df = df[['class', 'tweet']]  # 'class' is the label, 'tweet' is the text
df.dropna(inplace=True)

# 3. Download NLTK stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# 4. Text preprocessing
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r'\@w+|\#','', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text

df['clean_text'] = df['tweet'].apply(clean_text)

# 5. Train-Test split
X_train, X_test, y_train, y_test = train_test_split(df['clean_text'], df['class'], test_size=0.2, random_state=42)

# 6. TF-IDF Vectorization
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 7. Train model
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# 8. Evaluate model
y_pred = model.predict(X_test_tfidf)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# 9. Save model and vectorizer
joblib.dump(model, "hate_speech_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

# 10. Predict on new text (optional)
def predict_text(text):
    cleaned = clean_text(text)
    vec = vectorizer.transform([cleaned])
    return model.predict(vec)[0]

# Example
print(predict_text("I hate you!"))  # Should return class 0 or 1

"""Sample Test Text ✅"""

# Sample test texts
test_texts = [
    "I hate you",
    "You are amazing",
    "Go to hell!",
    "I respect everyone",
    "You are the worst person ever",
    "Let's spread kindness"
]

# Convert to TF-IDF format
test_texts_tfidf = vectorizer.transform(test_texts)

# Predict
predictions = model.predict(test_texts_tfidf)

# Display results
for text, pred in zip(test_texts, predictions):
    print(f"Text: {text} --> Prediction: {'Hate Speech' if pred == 1 else 'Not Hate Speech'}")



new_text = ["i hate you"]  # Change this text
new_text_tfidf = vectorizer.transform(new_text)
prediction = model.predict(new_text_tfidf)
print("Prediction:", "Hate Speech" if prediction[0] == 1 else "Not Hate Speech")