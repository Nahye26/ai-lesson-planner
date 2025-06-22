import streamlit as st
from transformers import pipeline

# Hugging Face 감정분석 파이프라인 로드
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

sentiment_model = load_sentiment_model()

def analyze_sentiment(text):
    result = sentiment_model(text)
    label = result[0]['label']
    # 긍정/부정 분류
    if label in ['1 star', '2 stars']:
        return "부정"
    elif label in ['4 stars', '5 stars']:
        return "긍정"
    else:
        return "중립"
