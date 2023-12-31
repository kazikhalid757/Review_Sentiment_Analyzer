
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential

data = pd.read_csv(r"Restaurant_Reviews.csv")

# Extract 'review_text' and 'sentiment' columns from the DataFrame
reviews = data['review_text'].tolist()
sentiments = data['sentiment'].tolist()

# Create and fit the tokenizer
tokenizer = Tokenizer()
tokenizer.fit_on_texts(reviews)
vocab_size = len(tokenizer.word_index) + 1

X = tokenizer.texts_to_sequences(reviews)
X = pad_sequences(X, padding='post')

# Convert sentiments to a numpy array
sentiments = np.array(sentiments)

# Build the model
model = Sequential()
model.add(Embedding(vocab_size, 100, input_length=X.shape[1]))
model.add(LSTM(100))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X, sentiments, epochs=5, batch_size=64, validation_split=0.2)


new_review = "This product is great! I love it."
new_review_seq = tokenizer.texts_to_sequences([new_review])
new_review_seq = pad_sequences(new_review_seq, padding='post', maxlen=X.shape[1])
predicted_sentiment = model.predict(new_review_seq)[0][0]

if predicted_sentiment > 0.5:
    prediction = "positive"
else:
    prediction = "negative"

predicted_sentiments = model.predict(X)
positive_percentage = sum(predicted_sentiments > 0.5) / len(predicted_sentiments) * 100
negative_percentage = 100 - positive_percentage

reviews_with_predictions = [(reviews[i], predicted_sentiments[i][0]) for i in range(len(reviews))]
reviews_with_predictions.sort(key=lambda x: x[1], reverse=True)

top_positive_reviews = [review for review, _ in reviews_with_predictions[:5]]
top_negative_reviews = [review for review, _ in reviews_with_predictions[-5:]]

import streamlit as st

# Load and preprocess data, train model, etc. (Steps 1-5)

# Streamlit app
st.title("Sentiment Analysis and Reviews")

# Upload new dataset
uploaded_file = st.file_uploader("Upload a new dataset", type="csv")

if uploaded_file:
    new_data = pd.read_csv(uploaded_file)
    # Process new_data, predict sentiments, calculate percentages, and find top reviews (Steps 3-5)

    # Display results
    st.write(f"Positive Percentage: {positive_percentage:.2f}%")
    st.write(f"Negative Percentage: {negative_percentage:.2f}%")

    st.write("Top Positive Reviews:")
    for review in top_positive_reviews:
        st.write(review)

    st.write("Top Negative Reviews:")
    for review in top_negative_reviews:
        st.write(review)
