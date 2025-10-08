import requests
import streamlit as st
import time

@st.cache_data(show_spinner=False)
def query_esmfold(sequence: str):
    """
    Query ESMFold API with sequence and return (pdb, confidence_scores).
    Handles downtime and retries gracefully.
    """
    url = "https://api.esmatlas.com/foldSequence/v1/pdb/"
    headers = {"Content-Type": "text/plain"}

    for attempt in range(3):  # retry logic
        try:
            response = requests.post(url, data=sequence, headers=headers, timeout=30)

            if response.status_code == 200:
                pdb = response.text
                confidences = [80 for _ in sequence]  # Dummy plDDT scores
                return pdb, confidences

            elif response.status_code in (429, 503):  # busy or unavailable
                st.warning(f"ESMFold API unavailable (code {response.status_code}). Retrying ({attempt+1}/3)...")
                time.sleep(5)
                continue

            else:
                st.error(f"ESMFold API Error: {response.status_code}")
                return None, None

        except requests.exceptions.RequestException as e:
            st.warning(f"Connection error: {e}. Retrying ({attempt+1}/3)...")
            time.sleep(5)

    st.error("ESMFold API is temporarily unavailable. Please try again later.")
    return None, None
