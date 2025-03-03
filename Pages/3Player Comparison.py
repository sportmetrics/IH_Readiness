import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Backend Stuff
st.set_page_config(layout="wide")

@st.cache_data
def load_players_data(players):
    player_data = load_data()
    player_data = player_data[(player_data['Name'].isin(players)) |
                              (player_data['assignedLine'].isin(players)) |
                              ((player_data['Position'] == 'D') & ('Defenders' in players)) |
                              ((player_data['Position'] == 'G') & ('Goalkeepers' in players)) |
                              ((player_data['Position'] == 'W') & ('Wingers' in players)) |
                              ((player_data['Position'] == 'C') & ('Centers' in players))]
    return player_data

@st.cache_data
def load_data():
    list_test_data = pd.read_csv('Sources/merged_df.csv')
    return list_test_data

@st.cache_data
def read_groups():
    data_list = pd.read_csv('Sources/groups.csv').squeeze()
    return data_list

# Load data and groups
data = load_data()
groups = read_groups()
distPlayers = data["Name"].dropna().unique().tolist()
distPlayers.extend(list(groups.values) + ["Wingers", "Centers", "Defenders", "Goalkeepers"])

# Frontend Stuff
st.markdown("# Player Comparison")

# Player selection
selectedplayers = st.multiselect("Choose the players to compare", distPlayers)

# Toggle for absolute values
absVals = st.toggle("Use absolute Values for comparison")

# Season selection using segmented control
seasons = ['All'] + data['Season'].dropna().unique().tolist()
selected_seasons = st.segmented_control("Seasons", seasons, selection_mode="multi", default="All")

# Category selection
categories = ["Overall", "Speed", "Strength", "Endurance", "Fullbody-Strength", "Hip-Strength", "Shoulder-Strength"]
selected_category = st.selectbox("Choose the category", categories)

# Toggle for showing values instead of visualizations
show_values = st.toggle("Show values instead of visualisations")

if not selectedplayers:
    st.error("No players selected")
else:
    compData = load_players_data(selectedplayers)

    # Filter player data based on selected seasons
    if "All" not in selected_seasons:
        compData = compData[compData['Season'].isin(selected_seasons)]

    # Define metrics based on category
    if selected_category == "Speed":
        metrics = ['5_10_5', '10m Off', '20m Off', '30m Off'] if absVals else ['5_10_5_index', '10m Off_index', '20m Off_index', '30m Off_index']
    elif selected_category == "Strength":
        metrics = ['CMJ W/kg', 'SJ W/kg', 'SL CMJ L', 'SL CMJ R'] if absVals else ['CMJ W/kg_index', 'SJ W/kg_index', 'SL CMJ L_index', 'SL CMJ R_index']
    elif selected_category == "Endurance":
        metrics = ['WG Ppeak W/kg', '3min W/kg', 'WG Pavg W/kg'] if absVals else ['WG Ppeak W/kg_index', '3min W/kg_index', 'WG Pavg W/kg_index']
    elif selected_category == "Fullbody-Strength":
        metrics = ['IMTP'] if absVals else ['IMTP_index']
    elif selected_category == "Hip-Strength":
        metrics = ['AD Mx F 60 L', 'AD Mx F 60 R', 'AB Mx F 60 L', 'AB Mx F 60 R'] if absVals else ['AD Mx F 60 L_index', 'AD Mx F 60 R_index', 'AB Mx F 60 L_index', 'AB Mx F 60 R_index']
    elif selected_category == "Shoulder-Strength":
        metrics = ['SH Int L', 'SH Int R', 'SH Ext L', 'SH Ext R'] if absVals else ['SH Int L_index', 'SH Int R_index', 'SH Ext L_index', 'SH Ext R_index']
    elif selected_category == "Overall":
        metrics = ['Speed_index', 'Endurance_index', 'power_index'] if not absVals else ['Speed_index', 'Endurance_index', 'power_index']
    else:
        metrics = ['Speed_index', 'Endurance_index', 'power_index', 'Hip_index', 'IMTP_index', 'Shoulder_index'] if not absVals else [
            '5_10_5', '10m Off', '20m Off', '30m Off',
            'CMJ W/kg', 'SJ W/kg', 'SL CMJ L', 'SL CMJ R',
            'WG Ppeak W/kg', '3min W/kg', 'WG Pavg W/kg']

    # Display values or visualizations
    if show_values:
        st.table(compData[['Name', 'Date', 'Position'] + metrics])
    else:
        for metric in metrics:
            fig = px.bar(compData, x='Date', y=metric, color='Name', barmode='group', title=f'Comparison of {metric} over Time')

            # Add team average line
            team_avg = data.groupby('Date')[metric].mean().reset_index()
            fig.add_trace(go.Scatter(x=team_avg['Date'], y=team_avg[metric], mode='lines+markers', name='Team Average', line=dict(color='orange', dash='dash')))

            st.plotly_chart(fig, use_container_width=True)