# This file is based on: https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/app.py

"""An example of showing geographic data."""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
from io import StringIO
from google.oauth2 import service_account
from google.cloud.vision import AnnotateImageResponse, ImageAnnotatorClient, Feature
import base64
from src.utils import draw_annotations_on_image

credentials = service_account.Credentials.from_service_account_file(
    './gcp_secrets/service_account_key.json')
client = ImageAnnotatorClient(credentials=credentials)


ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg']
ALLOWED_TEXT_EXTENSIONS = ['txt', 'csv', 'xlsx', 'xls']
st.title("Example application")
st.markdown(
    """
This is a demo application to test the features of Streamlit and how it can work together with the Google cloud ecosystem
"""
)




def transmit_vision_request(image):
    response = client.annotate_image({
        'image': {'content': base64.b64encode(image.getvalue()).decode('utf-8')},
        'features': [{'type_': Feature.Type.OBJECT_LOCALIZATION}]
    })
    return AnnotateImageResponse.to_dict(response)


def run():

    uploaded_file = st.file_uploader(
        "Choose a file", type=ALLOWED_IMAGE_EXTENSIONS+ALLOWED_TEXT_EXTENSIONS)
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]

        if file_extension in ALLOWED_TEXT_EXTENSIONS:
            uploaded_file_utf_8 = StringIO(
                uploaded_file.getvalue().decode('utf-8', 'replace'))

            if file_extension == 'txt':

                # To convert to a string based IO:
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

                # To read file as string:
                string_data = stringio.read()
                dataframe = pd.read_csv(uploaded_file_utf_8)

            else:

                # Can be used wherever a "file-like" object is accepted:
                dataframe = pd.read_csv(uploaded_file_utf_8)

            if st.checkbox("Show uploaded data", False):
                st.subheader(
                    "Uploaded Data"
                )
                st.write(dataframe)

        elif uploaded_file.name.split(".")[-1] in ALLOWED_IMAGE_EXTENSIONS:
            if st.checkbox("Show uploaded image", False):
                st.subheader(
                    "Uploaded Image"
                )
                st.image(uploaded_file)
            if st.button("Send request"):
                annotations = transmit_vision_request(uploaded_file)
                im = draw_annotations_on_image(uploaded_file, annotations)
                st.image(im)

    
if __name__ == "__main__":
    run()

