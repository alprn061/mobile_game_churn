import streamlit as st
import pandas as pd
from src.data_prep import load_data

# Title
st.title("Mobile Game Churn Analysis")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Dataset Preview:")
    st.dataframe(df.head())


# Load dataset from local if available
elif "data/dev.csv":
    df = load_data("data/dev.csv")
    st.write("Using default dataset:")
    st.dataframe(df.head())




# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["EDA", "Model Prediction"])




if page == "EDA":
    st.subheader("Exploratory Data Analysis")
    st.write("Dataset Summary:")
    st.write(df.describe())


elif page == "Model Prediction":
    st.subheader("Churn Prediction Model")
    st.write("Model will be integrated here...")
