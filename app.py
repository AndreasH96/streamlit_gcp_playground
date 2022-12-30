# This file is based on: https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/app.py

"""An example of showing geographic data."""

import streamlit as st
import pandas as pd
from io import StringIO
from src.utils import drawAnnotationsOnImage, styleTextBySentiment
from src.gcp_requests import transmitTextSentimentRequest,transmitVisionRequest

ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg']
ALLOWED_TEXT_EXTENSIONS = ['txt', 'csv', 'xlsx', 'xls']
st.title("Example application")
st.markdown(
    """
This is a demo application to test the features of Streamlit and how it can work together with the Google cloud ecosystem
"""
)


def handle_tabular_input(uploaded_file):
    uploaded_file_utf_8 = StringIO(
        uploaded_file.getvalue().decode('utf-8', 'replace'))

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file_utf_8)

    if st.checkbox("Show uploaded data", False):
        st.subheader(
            "Uploaded Data"
        )
        st.write(dataframe)


def handle_image_input(uploaded_file):
    if st.checkbox("Show uploaded image", False):
        st.subheader(
            "Uploaded Image"
        )
        st.image(uploaded_file)
    if st.button("Send request"):
        annotations = transmitVisionRequest(uploaded_file)
        im = drawAnnotationsOnImage(uploaded_file, annotations)
        st.image(im)


def run():
    st.subheader("Image object annotator")
    uploaded_file = st.file_uploader(
        "Choose a file", type=ALLOWED_IMAGE_EXTENSIONS+ALLOWED_TEXT_EXTENSIONS)
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]
        if file_extension in ALLOWED_TEXT_EXTENSIONS:
            handle_tabular_input(uploaded_file)
        elif uploaded_file.name.split(".")[-1] in ALLOWED_IMAGE_EXTENSIONS:
            handle_image_input(uploaded_file)

    st.subheader("Text sentiment analysis")
    text_input = st.text_input("What did you think of our product? Please write a review")
    if text_input and len(text_input.replace(" ","")) > 10:
        sentiment_response = transmitTextSentimentRequest(text_input)
        styled_text = styleTextBySentiment(text_input,sentiment_response)

        st.subheader("Sentiment results:")
        st.write(styled_text)


        #


if __name__ == "__main__":
    run()
