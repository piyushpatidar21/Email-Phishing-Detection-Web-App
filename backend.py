import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

# Load and clean dataset
data = pd.read_csv("spam_mail.csv")
data.drop_duplicates(inplace=True)
data['Category'] = data['Category'].replace(['ham', 'spam'], ['Not Spam', 'Spam'])

# Train-Test Split
mess = data["Masseges"]
cat = data['Category']

(mess_train, mess_test, cat_train, cat_test) = train_test_split(mess, cat, test_size=0.2)

# Vectorization
cv = CountVectorizer(stop_words='english')
features = cv.fit_transform(mess_train)

# Train Model
model = MultinomialNB()
model.fit(features, cat_train)

# Prediction Function
def predict(message):
    if not message.strip():
        return "Please enter a valid message."

    valid_words = ["lottery", "claim reward", "OTP", "gift", "cash prices", "account credited", "$", "won", "free", "amount"]
    for i in valid_words:
        if i in message:
            return "Spam"

    input_message = cv.transform([message]).toarray()
    result = model.predict(input_message)
    return result[0]
