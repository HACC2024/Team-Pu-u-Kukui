import streamlit as st
import pandas as pd
import plotly.express as px

from streamlit_extras.dataframe_explorer import dataframe_explorer

from style_helper import apply_custom_style

def main():
    apply_custom_style()
            
    st.header("Device Access")

    df = pd.read_excel("data/acs2022_5yr_counties_hi.xlsx")

    internet_df = pd.concat([df.iloc[0:2], df.iloc[170:174]], ignore_index=True)

    filtered_df = dataframe_explorer(internet_df, case=False)
    st.dataframe(internet_df, use_container_width=True)
    
if __name__ == "__main__":
    main()
