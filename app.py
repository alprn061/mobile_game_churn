import streamlit as st
import pandas as pd
from src.st import category_select, categories, level_slct_index, level_slct, adjust_sequence
from src.data_prep import load_data

# Load dataset
level_seq = load_data("data/level_seq.csv")

# Precompute level_counts
level_counts = level_seq.groupby(["level_id", "f_success"]).size().unstack()

# Streamlit UI
st.title("Game Level Analysis Dashboard")

# User selects category
category = st.selectbox("Select Category:", categories)

# User selects level range
lvl_start, lvl_end = st.slider("Select Level Range:", min_value=int(level_seq["level_id"].min()), 
                                                  max_value=int(level_seq["level_id"].max()), 
                                                  value=(int(level_seq["level_id"].min()), int(level_seq["level_id"].max())))

# Call category function (Bu artık otomatik olarak `st.pyplot(fig)` içeriyor)
category_select(category, lvl_start, lvl_end, level_counts, level_seq)
