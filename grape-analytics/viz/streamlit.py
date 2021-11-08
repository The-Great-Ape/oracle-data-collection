import streamlit as st
import pandas as pd
import os

options_paths = [
    os.path.join(dp, f)
    for dp, dn, filenames in os.walk("../metrics/")
    for f in filenames
    if os.path.splitext(f)[1] == ".csv"
]
options_list = []
options = {}

for i in range(len(options_paths)):
    key = options_paths[i].split("/")[-1].split("_")[0]
    less_values = [x for x in options_paths if key in x]
    if less_values not in options_list:
        options_list.append(less_values)
    for i in range(len(options_list)):
        key = options_list[i][0].split("/")[-1].split("_")[0]
        options[key] = options_list[i]

st.title("Grape Data Visualizations")
selected = st.multiselect("Select communities", options.keys())
if selected:
    for selection in selected:
        params = options[selection]
        option = {}
        for i in range(2):
            single_option = [param.split("_")[1].split(".")[0] for param in params][i]
            option[params[i]] = single_option
        st.subheader(selection)
        toviz = st.multiselect(
            "Select dataframes", params, format_func=lambda x: option[x], key=selection
        )
        if toviz:
            for viz in toviz:
                df = pd.read_csv(viz)
                st.dataframe(df)
