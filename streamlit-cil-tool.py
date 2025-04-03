import streamlit as st
import pandas as pd
import numpy as np
from functions import estimate_ci, cal_average_birth_prev, estimate_pooled_birth_prev_inverse, cal_Q_I2

st.set_page_config(page_title="Pooled Birth Prevalence Estimation Tool", layout="centered")
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
        # avg_prev = cal_average_birth_prev(df)
        # pooled_prev = estimate_pooled_birth_prev_inverse(df)
        q_i2_stats = cal_Q_I2(df)

        # Display results
        results_ci2 = results_ci.drop(columns=['margin_of_error', 'margin_of_error_100k'], axis=1, inplace=False)
        results_ci2['birth_prevalence'] = results_ci['birth_prevalence'].apply(lambda x: f"{x:.2e}") # Format to scientific notation
        st.write("**95% CI of Birth Prevalence per Study:**", results_ci2)

        selected_cols = ['average birth prevalence_100k', '95CI lower bound average', '95CI upper bound average',
                         'pooled birth prevalence (inverse) per 100K', '95 CI, lower_bound (inverse)', '95 CI, upper_bound (inverse)',
                         'Q_statistic', 'freedom_degree', 'I2_statistic']
        q_i2_stats2 = q_i2_stats.loc[0, selected_cols]
        # q_i2_stats3 = pd.DataFrame(q_i2_stats2)
        # q_i2_stats3.rename(columns={0: 'Value'}, inplace=True)
        q_i2_stats2 = q_i2_stats2.reset_index()
        q_i2_stats2.rename(columns={'index': 'Statistic'}, inplace=True)
        q_i2_stats3 = pd.DataFrame(q_i2_stats2)
        q_i2_stats3.rename(columns={0: 'Value'}, inplace=True)
        # q_i2_stats3

        st.write("**Pooled Prevalence:**", q_i2_stats3)

        # Optional: Save results to a downloadable CSV
        if st.button("Download CI Results as CSV"):
            q_i2_stats3.to_csv("q_i2_stats3.csv", index=False)
            with open("q_i2_stats3.csv", "rb") as f:
                st.download_button("Click to Download", f, file_name="q_i2_stats3.csv")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Awaiting CSV file upload...")
