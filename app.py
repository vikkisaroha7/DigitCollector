import streamlit as st
st.write("Available secret sections:", list(st.secrets.keys()))

st.set_page_config(
    page_title="AI Deep Learning Laboratory",
    page_icon="🧠",
    layout="wide"
)

st.title("MNIST Hand written digit classifer app")

st.markdown("""
Welcome to the **AI Deep Learning Laboratory**.

Use the navigation menu on the left to explore:

- 🏠 Dashboard
- ✍️ Predict Digit
- 🧠 Train Model
- 🔍 CNN Architecture
- 📊 Analytics
""")

st.info("Select a page from the left sidebar.")