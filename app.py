import streamlit as st
import numpy as np
import pickle
import pandas as pd
from src.st import category_select, categories, level_slct_index, level_slct, adjust_sequence
from src.data_prep import load_data

# set the page layout
st.set_page_config(layout="wide")

# add banner
st.image("banner.jpg", use_container_width=True)

# Load dataset
level_seq = load_data("data/level_seq.csv")
level_seq_eng = pickle.load(open("data/level_seq_eng.pkl", "rb"))

# Precompute level_counts
level_counts = level_seq.groupby(["level_id", "f_success"]).size().unstack()


# Streamlit Layout
col1, col2 = st.columns(2)

with col1:
    # Streamlit UI
    st.title("🎮 Game Level Analysis")

    # User selects category
    category = st.selectbox("Select Category:", categories)

    # User selects level range
    lvl_start, lvl_end = st.slider("Select Level Range:", min_value=int(level_seq["level_id"].min()), 
                                                    max_value=int(level_seq["level_id"].max()), 
                                                    value=(int(level_seq["level_id"].min()), int(level_seq["level_id"].max())))

    # Call category function 
    category_select(category, lvl_start, lvl_end, level_counts, level_seq)


with col2:
    st.title("Churn Prediction")

    st.write("Enter player statistics to predict churn probability:")

    # load the model
    with  open("models/random_forest.pkl", "rb") as model_file:
        model = pickle.load(model_file)


    # take input

    max_level = st.number_input("User Level", 
                            min_value=float(level_seq_eng["max_level"].min()), 
                            max_value=float(level_seq_eng["max_level"].max()), 
                            value=float(level_seq_eng["max_level"].mean()))
    user_success_rate = st.number_input("User Success Rate", 
                                    min_value=float(level_seq_eng["user_success_rate"].min()), 
                                    max_value=float(level_seq_eng["user_success_rate"].max()), 
                                    value=float(level_seq_eng["user_success_rate"].mean()))

    user_avg_duration = st.number_input("User Avg Duration", 
                                    min_value=float(level_seq_eng["user_avg_duration"].min()), 
                                    max_value=float(level_seq_eng["user_avg_duration"].max()), 
                                    value=float(level_seq_eng["user_avg_duration"].mean()))

    ## these values will be used as average, will not take input
    level_avg_reststep = level_seq_eng["level_avg_reststep"].mean()    
    total_used_help = level_seq_eng["total_used_help"].mean()
    user_help_rate = level_seq_eng["user_help_rate"].mean()
    most_played_day	= level_seq_eng["most_played_day"].mean()
    most_played_hour	= level_seq_eng["most_played_hour"].mean()



    # Feature names
    input_features = pd.DataFrame([[
        max_level, 
        user_success_rate, 
        user_avg_duration, 
        level_avg_reststep, 
        total_used_help, 
        user_help_rate, 
        most_played_day, 
        most_played_hour
    ]], columns=["max_level", "user_success_rate", "user_avg_duration", 
                "level_avg_reststep", "total_used_help", "user_help_rate", 
                "most_played_day", "most_played_hour"])




    # predict
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

    if st.button("Predict"):
        prediction = model.predict(input_features)
        probability = model.predict_proba(input_features)[0][1] 

        churn_status = "🔴 User will churn 🚨" if prediction[0] == 1 else "🟢 User will not churn ✅"
        st.subheader(f"Result: {churn_status}")
        st.write(f"Churn Probability: {probability:.2%}")
    st.markdown("</div>", unsafe_allow_html=True)


# Add summary metrics to bottom-right corner
st.markdown("---")
st.markdown("### Game Overview Metrics")
with st.container():
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", level_seq_eng["user_id"].nunique())
    col2.metric("Average Level Duration", f"{level_seq_eng['user_avg_duration'].mean().round(2)} Seconds")
    col3.metric("Most Played Hour", level_seq_eng.groupby("most_played_hour").size().idxmax())



