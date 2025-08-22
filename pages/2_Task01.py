import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

st.title("This is the task 2 route")
st.subheader("📊 Task 1: Predict Processing Time (minutes)")
st.divider()
st.write("Upload input file or enter values manually to predict `true_processing_time_minutes`.")

# Manual Input
with st.expander("🔹 Enter Input Manually"):
    date = st.date_input("Date")
    time = st.time_input("Time")
    task_id = st.text_input("Task ID")

    if st.button("Predict Processing Time"):
        # Convert into feature vector (adjust preprocessing as needed)
        features = np.array([[date.year, date.month, date.day,
                              time.hour, time.minute, hash(task_id) % 1000]])
        prediction = task1_model.predict(features)

        result_df = pd.DataFrame({
            "row_id": ["manual_input_task1"],
            "true_processing_time_minutes": [prediction[0]]
        })

        st.write("### ✅ Prediction Result")
        st.dataframe(result_df, use_container_width=True)

# Batch Input
with st.expander("📂 Upload CSV for Batch Predictions"):
    uploaded_file = st.file_uploader("Upload Task 1 CSV", type=["csv"], key="task1")

    if uploaded_file is not None:
        input_df = pd.read_csv(uploaded_file)
        st.write("### 🔎 Uploaded Data Preview")
        st.dataframe(input_df.head(), use_container_width=True)

        if st.button("Run Task 1 Predictions"):
            X = input_df.drop(columns=["row_id"], errors="ignore")
            preds = task1_model.predict(X)

            result_df = pd.DataFrame({
                "row_id": input_df["row_id"],
                "true_processing_time_minutes": preds
            })

            st.write("### ✅ Batch Prediction Results")
            st.dataframe(result_df, use_container_width=True)

            # --- Chart: Distribution of Processing Times ---
            st.write("### 📊 Distribution of Predicted Processing Times")
            fig, ax = plt.subplots()
            ax.hist(preds, bins=10, color="skyblue", edgecolor="black")
            ax.set_xlabel("Processing Time (minutes)")
            ax.set_ylabel("Frequency")
            ax.set_title("Predicted Processing Time Distribution")
            st.pyplot(fig)

            csv = result_df.to_csv(index=False).encode("utf-8")
            st.download_button("💾 Download Task 1 Predictions", csv, "task1_predictions.csv", "text/csv")

