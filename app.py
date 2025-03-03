import pandas as pd
import streamlit as st
import os


pg = st.navigation([st.Page("Pages/0Overview.py"), st.Page("Pages/1Team Analysis.py"), st.Page("Pages/2Player Analysis.py"), st.Page("Pages/3Player Comparison.py"), st.Page("Pages/4Lineup Configuration.py")])
pg.run()
