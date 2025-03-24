import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from src.data_prep import load_data, total_ratio

level_seq = load_data("data/level_seq.csv")
level_counts = level_seq.groupby(["level_id", "f_success"]).size().unstack()
level_counts = total_ratio(level_counts)
categories = ["Success & Fail Attempts", "Average Duration", "Average Rest Steps", "Average Duration2", "Average Rest Steps2"]

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
        data = level_counts.loc[lvl_start:lvl_end].reset_index()
        data_melted = data.melt(id_vars="level_id", value_vars=[0, 1], var_name="Success/Fail", value_name="Total")
        data_melted["selected"] = data_melted["level_id"].between(lvl_start, lvl_end)

        fig = px.bar(data_melted, 
                     x="level_id", 
                     y="Total", 
                     color="Success/Fail", 
                     color_discrete_map={0: "red", 1: "green"},
                     title="Success Distribution per Level")

        fig.update_layout(xaxis_title="Level", 
                          yaxis_title="Total",
                          xaxis=dict(tickangle=-45))
                          
        st.plotly_chart(fig, use_container_width=True)

    elif category == "Average Duration":
        data = level_slct(lvl_start, lvl_end, sequence, level_seq) 
        avg_duration = data.groupby("level_id", as_index=False)["f_duration"].mean()

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(x="level_id", y="f_duration", data=avg_duration, ax=ax)
        ax.set_xlabel("Level")
        ax.set_ylabel("Avg Duration")
        ax.set_title("Average Level Duration per Level")
        st.pyplot(fig)  

    elif category == "Average Rest Steps":
        data = level_slct(lvl_start, lvl_end, sequence, level_seq)
        avg_rest = data.groupby("level_id", as_index=False)["f_reststep"].mean()

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(x="level_id", y="f_reststep", data=avg_rest, ax=ax)
        ax.set_xlabel("Level")
        ax.set_ylabel("Avg Rest Steps")
        ax.set_title("Average Rest Steps per Level")
        st.pyplot(fig)  

    
    elif category == "Average Duration2":
        data = level_slct(lvl_start, lvl_end, sequence, level_seq)
        avg_duration = data.groupby("level_id", as_index=False)["f_duration"].mean()

        fig = px.line(avg_duration, x="level_id", y="f_duration",
                    title="Average Level Duration per Level",
                    labels={"level_id": "Level", "f_duration": "Avg Duration"},
                    template="plotly_dark")  # Alternatif: "ggplot2", "seaborn", "simple_white"
        
        st.plotly_chart(fig, use_container_width=True)

    elif category == "Average Rest Steps2":
        data = level_slct(lvl_start, lvl_end, sequence, level_seq)
        avg_duration = data.groupby("level_id", as_index=False)["f_reststep"].mean()

        fig = px.line(avg_duration, x="level_id", y="f_reststep",
                    title="Average Rest Steps per Level",
                    labels={"level_id": "Level", "f_reststep": "Avg Rest Steps"},
                    template="ggplot2")  # Alternatif: "ggplot2", "seaborn", "simple_white"
        
        st.plotly_chart(fig, use_container_width=True)