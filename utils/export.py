import streamlit as st
import io

def export_csv(results_df):
    buffer = io.StringIO()
    results_df.to_csv(buffer, index=False)
    st.download_button(
        label="📥 Export Results as CSV",
        data=buffer.getvalue(),
        file_name="results.csv",
        mime="text/csv",
    )
