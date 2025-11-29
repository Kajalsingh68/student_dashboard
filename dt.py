import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

# Page Configuration
st.set_page_config(page_title="Student Performance EDA", layout="wide", page_icon="🎓")

# Header
st.title("🎓 Student Performance EDA Dashboard")
st.markdown("Explore and visualize student marks interactively using this dashboard.")

# Sidebar Section
st.sidebar.header("⚙️ Data Input Options")

# Option to choose file input method
data_source = st.sidebar.radio("Select Data Source", ["📂 Upload CSV", "💾 Enter File Path"])

df = None

# === Option 1: Upload CSV ===
if data_source == "📂 Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload your student CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")

# === Option 2: Local File Path ===
else:
    file_path = st.sidebar.text_input("Enter the full file path:", "data_science_student_marks.csv")
    if st.sidebar.button("Load Data"):
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            st.success(f"✅ File loaded successfully from: `{file_path}`")
        else:
            st.error("❌ File not found! Please check the path and try again.")

# === When data is loaded ===
if df is not None:
    # Show dataset preview
    st.subheader("📊 Dataset Preview")
    st.dataframe(df, use_container_width=True)

    # Basic metrics
    st.subheader("🧾 Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Average Age", round(df['age'].mean(), 1))
    col4.metric("Average Overall Marks", round(df.iloc[:, 3:].mean().mean(), 1))

    # Identify numeric subject columns
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    numeric_cols = [col for col in numeric_cols if col not in ['student_id', 'age']]

    st.divider()
    st.subheader("📈 Subject-wise Analysis")

    subject = st.selectbox("Select a subject for analysis", numeric_cols)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(df, x="location", y=subject, color="location",
                     title=f"{subject} Scores by Location",
                     text_auto=True, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.box(df, x="location", y=subject, color="location",
                      title=f"{subject} Score Distribution",
                      template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("🏆 Overall Performance Comparison")

    avg_marks = df[numeric_cols].mean().sort_values(ascending=False).reset_index()
    avg_marks.columns = ['Subject', 'Average Marks']

    fig3 = px.bar(avg_marks, x='Subject', y='Average Marks', color='Subject',
                  title='Average Marks per Subject', text_auto=True,
                  template="plotly_white")
    st.plotly_chart(fig3, use_container_width=True)

    st.divider()
    st.subheader("📊 Correlation Heatmap")

    corr = df[numeric_cols].corr()
    fig4 = px.imshow(corr, text_auto=True, color_continuous_scale='Blues',
                     title="Correlation Between Subjects")
    st.plotly_chart(fig4, use_container_width=True)

    st.divider()
    st.subheader("🧍 Student Performance Overview")

    df["Total_Marks"] = df[numeric_cols].sum(axis=1)
    df["Average_Marks"] = df["Total_Marks"] / len(numeric_cols)

    fig5 = px.bar(df, x="student_id", y="Average_Marks", color="location",
                  title="Average Marks per Student", text_auto=True,
                  template="plotly_white")
    st.plotly_chart(fig5, use_container_width=True)

else:
    st.warning("⚠️ Please upload a CSV file or provide a valid file path to begin.")
    st.info("Example CSV format:")
    example = pd.DataFrame({
        "student_id": [4, 5, 6],
        "location": ["Sydney", "Tokyo", "Berlin"],
        "age": [24, 24, 22],
        "sql_marks": [95, 99, 72],
        "excel_marks": [99, 95, 70],
        "python_marks": [87, 89, 99],
        "power_bi_marks": [82, 86, 79],
        "english_marks": [75, 82, 77]
    })
    st.dataframe(example, use_container_width=True)
