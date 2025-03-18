import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_prep import load_data, total_ratio

level_seq = load_data("data/level_seq.csv")
level_counts = level_seq.groupby(["level_id", "f_success"]).size().unstack()
level_counts = total_ratio(level_counts)
categories = ["Success & Fail Attempts", "Average Duration", "Average Rest Steps"]

def adjust_sequence(lvl_start, lvl_end):
    level_range = lvl_end - lvl_start
    if level_range < 100:
        return 2
    elif level_range < 300:
        return 5
    elif level_range < 700:
        return 10
    elif level_range < 1000:
        return 15
    else:
        return 17
    
def level_slct_index(lvl_start, lvl_end, seq, level_counts):
    """Belirli bir aralıktaki level'ları sequence'a göre filtreler (Success & Fail için)"""
    return level_counts.loc[lvl_start:lvl_end:seq]

def level_slct(lvl_start, lvl_end, seq, level_seq):
    """Belirli bir aralıktaki level'ları sequence'a göre filtreler (Ortalama değerler için)"""
    return level_seq[level_seq["level_id"].isin(np.arange(lvl_start, lvl_end, seq))]

def category_select(category, lvl_start, lvl_end, level_counts, level_seq):
    sequence = adjust_sequence(lvl_start, lvl_end)  

    if category == "Success & Fail Attempts":
        data = level_slct_index(lvl_start, lvl_end, sequence, level_counts) 

        fig, ax = plt.subplots(figsize=(12, 6))
        data[[0, 1]].plot(kind="bar", stacked=True, color=["red", "green"], ax=ax)
        ax.set_xlabel("Level")
        ax.set_ylabel("Total")
        ax.set_title("Success Distribution per Level")
        ax.legend(title="Success/Fail")
        st.pyplot(fig)  # ✅ fig tanımlandı ve Streamlit'e gönderildi

    elif category == "Average Duration":
        data = level_slct(lvl_start, lvl_end, sequence, level_seq) 
        avg_duration = data.groupby("level_id", as_index=False)["f_duration"].mean()

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(x="level_id", y="f_duration", data=avg_duration, ax=ax)
        ax.set_xlabel("Level")
        ax.set_ylabel("Avg Duration")
        ax.set_title("Average Level Duration per Level")
        st.pyplot(fig)  # ✅ fig tanımlandı ve Streamlit'e gönderildi

    elif category == "Average Rest Steps":
        data = level_slct(lvl_start, lvl_end, sequence, level_seq)
        avg_rest = data.groupby("level_id", as_index=False)["f_reststep"].mean()

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(x="level_id", y="f_reststep", data=avg_rest, ax=ax)
        ax.set_xlabel("Level")
        ax.set_ylabel("Avg Rest Steps")
        ax.set_title("Average Rest Steps per Level")
        st.pyplot(fig)  # ✅ fig tanımlandı ve Streamlit'e gönderildi
