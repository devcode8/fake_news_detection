import streamlit as st
import requests
import json

st.set_page_config(page_title="News Verification", page_icon="📰", layout="wide")

st.title("📰 News Verification System")
st.markdown("Analyze news headlines for authenticity using AI-powered fact-checking.")

API_ENDPOINT = "http://localhost:8080/news"

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Submit News for Analysis")
    
    news_input = st.text_area(
        "Enter news headline or article:",
        placeholder="Enter the news headline you want to verify...",
        height=100
    )
    
    if st.button("Analyze News", type="primary"):
        if news_input.strip():
            with st.spinner("Analyzing news..."):
                try:
                    payload = {"query": news_input.strip()}
                    response = requests.post(API_ENDPOINT, json=payload, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.last_result = result.get("msg", "No analysis result")
                        st.session_state.last_query = news_input.strip()
                        st.success("Analysis completed!")
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the news analysis service. Make sure the API is running on localhost:8080")
                except requests.exceptions.Timeout:
                    st.error("Request timed out. The analysis is taking longer than expected.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a news headline to analyze.")

with col2:
    st.header("Analysis Results")
    
    if hasattr(st.session_state, 'last_result') and hasattr(st.session_state, 'last_query'):
        st.subheader("Last Analyzed:")
        st.info(f"**Query:** {st.session_state.last_query}")
        
        st.subheader("Analysis Result:")
        result_text = st.session_state.last_result
        
        st.text_area("Detailed Analysis:", result_text, height=300, disabled=True)
    else:
        st.info("Submit a news headline for analysis to see results here.")

st.markdown("---")
st.markdown("**Note:** Make sure the news analysis API is running on `http://localhost:8080`")