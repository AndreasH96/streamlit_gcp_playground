from google.oauth2 import service_account
from google.cloud.vision import AnnotateImageResponse, ImageAnnotatorClient, Feature
from google.cloud.language_v1 import LanguageServiceClient, Document, AnalyzeEntitySentimentResponse
import base64
import streamlit as st

credentials = service_account.Credentials.from_service_account_file(
    './gcp_secrets/service_account_key.json')

@st.cache
def transmitVisionRequest(image):
    client = ImageAnnotatorClient(credentials=credentials)
    response = client.annotate_image({
        'image': {'content': base64.b64encode(image.getvalue()).decode('utf-8')},
        'features': [{'type_': Feature.Type.OBJECT_LOCALIZATION}]
    })
    return AnnotateImageResponse.to_dict(response)

@st.cache
def transmitTextSentimentRequest(text):
    client = LanguageServiceClient(credentials=credentials)
    # The text to analyze
    document = Document(
        content=text, type_=Document.Type.PLAIN_TEXT
    )

    # Detects the sentiment of the text
    sentiment = client.analyze_entity_sentiment(
        request={"document": document}
    )
    return AnalyzeEntitySentimentResponse.to_dict(sentiment)
