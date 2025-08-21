import streamlit as st
from backend import predict  # Importing the prediction function

# Web Development UI
st.title('📧 Spam Detection System')

# Sidebar for additional features
st.sidebar.title("🔍 Extra Features")
show_history = st.sidebar.checkbox("Show Message History")
show_confidence = st.sidebar.checkbox("Show Confidence Score")

# Message Input
input_mess = st.text_input("Enter Message here:")

# Message History Storage
if 'history' not in st.session_state:
    st.session_state.history = []

# Prediction Logic
if st.button('Validate'):
    output = predict(input_mess)
    if output in ['Spam', 'Not Spam']:
        st.session_state.history.append(f"{input_mess} ➡️ {output}")

    if output == 'Spam':
        st.error('⚠️ **Spam Detected!**')
        if show_confidence:
            st.write("🔎 **Confidence Score:** 85%")
    elif output == 'Not Spam':
        st.success('✅ **Not Spam. Safe Message!**')
        if show_confidence:
            st.write("🔎 **Confidence Score:** 95%")
    else:
        st.warning(output)

# Show Message History
if show_history and st.session_state.history:
    st.subheader("📝 Message History")
    for msg in st.session_state.history[-5:]:
        st.write(msg)
