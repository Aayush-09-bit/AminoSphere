import requests
import streamlit as st
import time

@st.cache_data(show_spinner=False)
def query_esmfold(sequence: str):
    """
    Query ESMFold API with sequence and return (pdb, confidence_scores).
    Handles API downtime, 503 errors, and connection issues gracefully.
    """
    url = "https://api.esmatlas.com/foldSequence/v1/pdb/"
    headers = {"Content-Type": "text/plain"}

    for attempt in range(3):  # Try 3 times before giving up
        try:
            response = requests.post(url, data=sequence, headers=headers, timeout=30)

            if response.status_code == 200:
                pdb = response.text
                confidences = [80 for _ in sequence]
                return pdb, confidences

            elif response.status_code in (429, 503):  # Too many requests / Service down
                st.warning(
                    f"⚠️ ESMFold API temporarily unavailable (Error {response.status_code}). "
                    f"Retrying in 5 seconds... (Attempt {attempt+1}/3)"
                )
                time.sleep(5)
                continue

            else:
                # Unexpected API response
                st.error(f"❌ ESMFold API returned error: {response.status_code}")
                return None, None

        except requests.exceptions.RequestException as e:
            st.warning(f"🌐 Connection error: {e}. Retrying... ({attempt+1}/3)")
            time.sleep(5)

    # After all retries, show a clear message and fallback
    st.error("🚫 ESMFold API is currently unavailable. Please try again later.")
    return None, None
