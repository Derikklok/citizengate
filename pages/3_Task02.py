import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

st.title("This is the task 2 route")
st.subheader("👥 Task 2: Predict Required Employees")
st.divider()
st.write("Upload input file or enter values manually to predict `true_required_employees`.")

# Manual Input
with st.expander("🔹 Enter Input Manually"):
    date = st.date_input("Date", key="date_task2")
    section_id = st.text_input("Section ID")

    if st.button("Predict Required Employees"):
        features = np.array([[date.year, date.month, date.day, hash(section_id) % 1000]])
        prediction = task2_model.predict(features)

        result_df = pd.DataFrame({
            "row_id": ["manual_input_task2"],
            "true_required_employees": [prediction[0]]
        })

        st.write("### ✅ Prediction Result")
        st.dataframe(result_df, use_container_width=True)

# Batch Input
with st.expander("📂 Upload CSV for Batch Predictions"):
    uploaded_file = st.file_uploader("Upload Task 2 CSV", type=["csv"], key="task2")

    if uploaded_file is not None:
        input_df = pd.read_csv(uploaded_file)
        st.write("### 🔎 Uploaded Data Preview")
        st.dataframe(input_df.head(), use_container_width=True)

        if st.button("Run Task 2 Predictions"):
            X = input_df.drop(columns=["row_id"], errors="ignore")
            preds = task2_model.predict(X)

            result_df = pd.DataFrame({
                "row_id": input_df["row_id"],
                "true_required_employees": preds
            })

            st.write("### ✅ Batch Prediction Results")
            st.dataframe(result_df, use_container_width=True)

            st.write("### 📊 Distribution of Predicted Employee Requirements")
            fig, ax = plt.subplots()
            pd.Series(preds).value_counts().sort_index().plot(kind="bar", ax=ax, color="salmon", edgecolor="black")
            ax.set_xlabel("Required Employees")
            ax.set_ylabel("Count")
            ax.set_title("Predicted Employee Requirement Distribution")
            st.pyplot(fig)

            csv = result_df.to_csv(index=False).encode("utf-8")
            st.download_button("💾 Download Task 2 Predictions", csv, "task2_predictions.csv", "text/csv")
