import streamlit as st
import pandas as pd
import numpy as np
from functions import estimate_ci, cal_average_birth_prev, estimate_pooled_birth_prev_inverse, cal_Q_I2

st.set_page_config(page_title="Birth Prevalence Estimation Tool", layout="centered")
st.title("🧮 Birth Prevalence Estimation Tool")

st.markdown("""
This tool estimates birth prevalence using uploaded data.
Please upload a CSV file in the correct format to begin.
""")

uploaded_file = st.file_uploader("Upload Input CSV File", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("File loaded successfully!")

        # Display the input data
        st.subheader("📄 Preview of Input Data")
        st.dataframe(df)

        # Run estimation functions
        st.subheader("📊 Estimation Results")
        results_ci = estimate_ci(df)
        avg_prev = cal_average_birth_prev(df)
        pooled_prev = estimate_pooled_birth_prev_inverse(df)
        q_i2_stats = cal_Q_I2(df)

        # Display results
        st.write("**Confidence Intervals:**")
        st.dataframe(results_ci)

        st.write("**Average Birth Prevalence:**", avg_prev)
        st.write("**Pooled Prevalence (Inverse Variance):**", pooled_prev)
        st.write("**Q and I² Statistics:**")
        st.dataframe(pd.DataFrame([q_i2_stats]))

        # Optional: Save results to a downloadable CSV
        if st.button("Download CI Results as CSV"):
            results_ci.to_csv("ci_results.csv", index=False)
            with open("ci_results.csv", "rb") as f:
                st.download_button("Click to Download", f, file_name="ci_results.csv")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Awaiting CSV file upload...")
