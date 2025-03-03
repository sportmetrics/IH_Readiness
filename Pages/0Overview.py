import pandas as pd
import streamlit as st
import os



#st.set_page_config(layout="wide")

# Get the absolute directory of the current file & set working directory
# script_dir = os.path.dirname(os.path.abspath(__file__))
# os.chdir(script_dir)


st.markdown("# Overview")

st.write("""
Welcome to the Performance Data Analysis Dashboard. Here's a brief overview of what you can do on each page:

- **Team Analysis**: View team-wide performance metrics and compare different teams against each other.

- **Player Analysis**: Dive into individual player statistics, track development, and performance trends over time.

- **Player Comparison**: Compare multiple players or groups across various performance areas.

- **Lineup Configuration**: Manage groups by creating, deleting, and assigning players to specific groups for better analysis.
""")
