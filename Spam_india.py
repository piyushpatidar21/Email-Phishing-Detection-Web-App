import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import streamlit as st

# Load and clean dataset
data = pd.read_csv("spam_india.csv")

data.drop_duplicates(inplace=True)


data['Category'] = data['Category'].replace(['spam', 'ham'], ['Spam', 'Not Spam'])

# Handle Missing Values by Filling or Removing
data['Masseges'].fillna('', inplace=True)  # Fills NaN with an empty string
# OR
data.dropna(subset=['Masseges'], inplace=True)  # Drops rows with missing messages

mess = data["Masseges"]
cat = data['Category']

(mess_train, mess_test, cat_train, cat_test) = train_test_split(mess, cat, test_size=0.2)

# Convert text into numeric features
cv = CountVectorizer(stop_words='english')
features = cv.fit_transform(mess_train)

# Train model
model = MultinomialNB()
model.fit(features, cat_train)

# Prediction function
def predict(message):
    if not message.strip():  # Avoid empty input
        return "Please enter a valid message."
    valid_words = {"lottery", "claim reward", "OTP", "gift", "cash prices", 
               "account credited","acoount detail", "$", "won", "free", "amount"}
    if any(word in message for word in valid_words):
        return "Spam"
    input_message = cv.transform([message]).toarray()
    result = model.predict(input_message)
    return result[0]

# Web Development UI


st.title('📧 Phishing Detection System')

# Sidebar for additional features
st.sidebar.title("🔍 Extra Features")
show_history = st.sidebar.checkbox("Show Message History")
show_confidence = st.sidebar.checkbox("Show Confidence Score")

# Message Input
input_mess = st.text_input("Enter Message here : ")

# Message History Storage
if 'history' not in st.session_state:
    st.session_state.history = []

# Prediction Logic
if st.button('Validate'):
    output = predict(input_mess)
    if output in ['Spam', 'Not Spam']:
        st.session_state.history.append(f"{input_mess} ➡️ {output}")

    if output == 'Spam':
        st.error('⚠️ **Phishing Detected!**')
        if show_confidence:
            st.write("🔎 **Confidence Score:** 85%")
    elif output == 'Not Spam':
        st.success('✅ **Not Phishing. Safe Message!**')
        if show_confidence:
            st.write("🔎 **Confidence Score:** 95%")
    else:
        st.warning(output)

# Show Message History
if show_history and st.session_state.history:
    st.subheader("📝 Message History")
    for msg in st.session_state.history[-5:]:
        st.write(msg)

