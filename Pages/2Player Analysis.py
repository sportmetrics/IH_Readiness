import streamlit as st
import pandas as pd
import random
import plotly as py
import plotly.graph_objs as go
import plotly.express as px

# Backend

# Page config
#st.set_page_config(layout="wide")

# Function to load Player data (cached)
@st.cache_data
def load_player_data(player):
    player_data = load_data()
    player_data = player_data[player_data['Name'] == player]
    return player_data

# Function to load all data (cached)
@st.cache_data
def load_data():
    list_test_data = pd.DataFrame()
    list_test_data = pd.read_csv('Sources/merged_df.csv')
    return list_test_data


# Load data & get distinct players
data = load_data()
distPlayers = data["Name"].dropna().unique().tolist()

# Frontend
st.markdown("# Player Analysis")

# Player selection
player = st.selectbox("Choose the player", distPlayers)

if player is None:
    st.error("Please select a player")
else:
    # Load player data
    player_data_test = load_player_data(player)
    player_position = player_data_test["Position"].iloc[0]  # Get player position for position average

    # Write player data into sidebar
    st.sidebar.image('Images/anonym.jpeg')
    st.sidebar.write("Name: " + str(player_data_test["Name"].iloc[0]))
    st.sidebar.write("Position: " + player_position)
    st.sidebar.write("Birthyear: " + str(player_data_test["Birthyear"].iloc[0]))

    try:
        st.sidebar.write("Height: " + str(player_data_test.loc[
                                                     (player_data_test["Date"] == player_data_test["Date"].max()) &
                                                     (player_data_test["Size"].notna()) &
                                                     (player_data_test["Size"] != 0), "Size"].iloc[0]) + " cm")
    except:
        st.sidebar.write("Height: N.A.")

    try:
        st.sidebar.write("Weight: " + str(player_data_test.loc[
                                                     (player_data_test["Date"] == player_data_test["Date"].max()) &
                                                     (player_data_test["Weight"].notna()) &
                                                     (player_data_test["Weight"] != 0), "Weight"].iloc[0]) + " kg")
    except:
        st.sidebar.write("Weight: N.A.")



    # Create columns to display data
    col1, col2 = st.columns([4, 5])

    # Readiness & Recommendation - Container (Left)
    with col1:
        container = st.container(border=True)
        container.markdown(
            """
            ### Readiness & Recommendations 
            <p style="font-size:14px; margin-top: -10px;">
                (based on latest test data)
            </p>
            """,
            unsafe_allow_html=True
        )

        try:
            container.markdown("""<b>Strongest Category:</b> """ + str(player_data_test.loc[
                                                  (player_data_test["Date"] == player_data_test["Date"].max()) &
                                                  (player_data_test["Best_Skill_Category"].notna()) &
                                                  (player_data_test["Best_Skill_Category"] != 0), "Best_Skill_Category"].iloc[0]), unsafe_allow_html=True)
        except:
            container.markdown("""<b>Strongest Category:</b> N.A.""", unsafe_allow_html=True)

        try:
            container.write("""<b>Weakest Category:</b> """ + str(player_data_test.loc[
                                                  (player_data_test["Date"] == player_data_test["Date"].max()) &
                                                  (player_data_test["Improvement_Recommendation_Category"].notna()) &
                                                  (player_data_test["Improvement_Recommendation_Category"] != 0), "Improvement_Recommendation_Category"].iloc[0]), unsafe_allow_html=True)
        except:
            container.write("""<b>Weakest Category:</b> N.A.""", unsafe_allow_html=True)

        # --- Calculate Physical Form ---
        latest_data = player_data_test[player_data_test["Date"] == player_data_test["Date"].max()]

        # Safely get indices, default to 0 if missing
        speed_index = latest_data["Speed_index"].fillna(0).values[0]
        power_index = latest_data["power_index"].fillna(0).values[0]
        endurance_index = latest_data["Endurance_index"].fillna(0).values[0]

        # Compute Physical Form as average
        physical_form_score = round((speed_index + power_index + endurance_index) / 3)

        # --- Calculate Injury Prevention Score ---
        hip_index = latest_data["Hip_index"].fillna(0).values[0]
        imtp_index = latest_data["IMTP_index"].fillna(0).values[0]
        shoulder_index = latest_data["Shoulder_index"].fillna(0).values[0]

        injury_prevention_score = round((hip_index + imtp_index + shoulder_index) / 3)

        # --- Create Two Columns for Gauges ---
        gauge_col1, gauge_col2 = container.columns(2)

        with gauge_col1:
            # Physical Form Gauge
            physical_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=physical_form_score,
                title={'text': "Physical Form", 'font': {'size': 16}},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 35], 'color': "red"},
                        {'range': [35, 55], 'color': "yellow"},
                        {'range': [55, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 3},
                        'thickness': 0.75,
                        'value': physical_form_score
                    }
                }
            ))

            physical_gauge.update_layout(
                width=150,
                height=200,
                margin=dict(t=10, b=10, l=10, r=10)
            )

            st.plotly_chart(physical_gauge, use_container_width=True, theme="streamlit", key="physical_form_gauge")

            # --- Radar Charts Below ---
            # Physical Radar Chart
            overall_categories = ['Speed', 'Strength', 'Endurance']

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=[speed_index, power_index, endurance_index],
                theta=overall_categories,
                fill='toself',
                name=player_data_test["Name"].iloc[0]
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=8)),
                    angularaxis=dict(rotation=60, tickfont=dict(size=8)),
                    bgcolor='rgba(0,0,0,0)'
                ),
                showlegend=False,
                width=150,
                height=150,
                margin=dict(t=5, b=5, l=0, r=0)
            )

            st.plotly_chart(fig, use_container_width=True, theme="streamlit", key="physical_radar")

        with gauge_col2:
            # Injury Prevention Gauge
            injury_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=injury_prevention_score,
                title={'text': "Injury Prevention", 'font': {'size': 16}},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 35], 'color': "red"},
                        {'range': [35, 55], 'color': "yellow"},
                        {'range': [55, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 3},
                        'thickness': 0.75,
                        'value': injury_prevention_score
                    }
                }
            ))

            injury_gauge.update_layout(
                width=150,
                height=200,
                margin=dict(t=5, b=5, l=10, r=10)
            )

            st.plotly_chart(injury_gauge, use_container_width=True, theme="streamlit", key="injury_prevention_gauge")



            # Injury Radar Chart
            injury_category = ['Hip', 'Fullbody (IMTP)', 'Shoulder']

            fig2 = go.Figure()
            fig2.add_trace(go.Scatterpolar(
                r=[hip_index, imtp_index, shoulder_index],
                theta=injury_category,
                fill='toself',
                name=player_data_test["Name"].iloc[0]
            ))

            fig2.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=8)),
                    angularaxis=dict(rotation=180, tickfont=dict(size=8)),
                    bgcolor='rgba(0,0,0,0)'
                ),
                showlegend=False,
                width=150,
                height=150,
                margin=dict(t=5, b=5, l=0, r=0)
            )

            st.plotly_chart(fig2, use_container_width=True, theme="streamlit", key="injury_radar")

    # Detail Analysis (Right)
    with col2:

        # Time horizon / seasons selection
        seasons = ['All'] + data['Season'].unique().tolist()
        selection = st.segmented_control("Seasons", seasons, selection_mode="multi", default="All")

        # Filter player data based on selected seasons (for bar charts)
        if "All" in selection:
            filtered_player_data = player_data_test  # No filtering if 'Overall' is selected
            filtered_team_data = data  # Team data without filtering
        else:
            filtered_player_data = player_data_test[player_data_test['Season'].isin(selection)]
            filtered_team_data = data[data['Season'].isin(selection)]

        # Toggle between absolute values and indices
        absVals = st.toggle("Use absolute Values for graphs")

        physical, injury = st.tabs(["Physical Form", "Injury Prevention"])

        # Function to add team and position averages
        def add_average_lines(fig, metric):
            # Team average calculation
            team_avg = filtered_team_data.groupby('Date')[metric].mean().reset_index()

            # Position average calculation
            position_avg = filtered_team_data[filtered_team_data['Position'] == player_position].groupby('Date')[
                metric].mean().reset_index()

            # Add team average line (blue)
            fig.add_trace(
                go.Scatter(
                    x=team_avg['Date'],
                    y=team_avg[metric],
                    mode='lines+markers',
                    name='Team Average',
                    line=dict(color='orange', width=2, dash='dash')
                )
            )

            # Add position average line (green)
            fig.add_trace(
                go.Scatter(
                    x=position_avg['Date'],
                    y=position_avg[metric],
                    mode='lines+markers',
                    name='Position Average',
                    line=dict(color='green', width=2, dash='dot')
                )
            )
            return fig

        # Physical perspective
        physical_perspective = physical.selectbox("Choose the perspective", ["Overall", "Speed", "Strength", "Endurance"])

        if physical_perspective == "Overall":
            metrics = ["Speed_index", "power_index", "Endurance_index"]
            for metric in metrics:
                fig = px.bar(filtered_player_data, x="Date", y=metric, title=f"Performance in {metric}")
                fig = add_average_lines(fig, metric)
                physical.plotly_chart(fig, use_container_width=True)

        elif physical_perspective == "Speed":
            if absVals:
                metrics = ["5_10_5", "10m Off", "20m Off", "30m Off"]
                y_label = "Seconds"
            else:
                metrics = ["5_10_5_index", "10m Off_index", "20m Off_index", "30m Off_index"]
                y_label = "Index of Exercise (0-100)"

            for metric in metrics:
                fig = px.bar(filtered_player_data, x="Date", y=metric, title=f"Speed Performance in {metric}")
                fig = add_average_lines(fig, metric)
                physical.plotly_chart(fig, use_container_width=True)

        elif physical_perspective == "Strength":
            if absVals:
                metrics = ["CMJ W/kg", "SJ W/kg", "SL CMJ L", "SL CMJ R"]
                y_label = "W/kg"
            else:
                metrics = ["CMJ W/kg_index", "SJ W/kg_index", "SL CMJ L_index", "SL CMJ R_index"]
                y_label = "Index of Exercise (0-100)"

            for metric in metrics:
                fig = px.bar(filtered_player_data, x="Date", y=metric, title=f"Strength Performance in {metric}")
                fig = add_average_lines(fig, metric)
                physical.plotly_chart(fig, use_container_width=True)

        elif physical_perspective == "Endurance":
            if absVals:
                metrics = ["WG Ppeak W/kg", "3min W/kg", "WG Pavg W/kg"]
                y_label = "W/kg"
            else:
                metrics = ["WG Ppeak_index", "WGPpeak W/kg_index", "3min MMP_index", "3min W/kg_index", "WG Pavg W/kg_index"]
                y_label = "Index of Exercise (0-100)"

            for metric in metrics:
                fig = px.bar(filtered_player_data, x="Date", y=metric, title=f"Endurance Performance in {metric}")
                fig = add_average_lines(fig, metric)
                physical.plotly_chart(fig, use_container_width=True)

        # Injury Perspective
        injury_perspective = injury.selectbox("Choose the perspective", ["Overall", "Fullbody-Strength", "Hip-Strength", "Shoulder-Strength"])

        if injury_perspective == "Overall":
            metrics = ["IMTP_index", "Hip_index", "Shoulder_index"]
            for metric in metrics:
                fig = px.bar(filtered_player_data, x="Date", y=metric, title=f"Injury Prevention: {metric}")
                fig = add_average_lines(fig, metric)
                injury.plotly_chart(fig, use_container_width=True)

        elif injury_perspective == "Fullbody-Strength":
            if absVals:
                metrics = ["IMTP"]
                y_label = "Newton"
            else:
                metrics = ["IMTP_index"]
                y_label = "Index of Exercise (0-100)"

            for metric in metrics:
                fig = px.bar(filtered_player_data, x="Date", y=metric, title=f"Fullbody Strength in {metric}")
                fig = add_average_lines(fig, metric)
                injury.plotly_chart(fig, use_container_width=True)

        elif injury_perspective == "Hip-Strength":
            if absVals:
                metrics = ["AD Mx F 60 L", "AD Mx F 60 R", "AB Mx F 60 L", "AB Mx F 60 R"]
                y_label = "Newton"
            else:
                metrics = ["AD Mx F 60 L_index", "AD Mx F 60 R_index", "AB Mx F 60 L_index", "AB Mx F 60 R_index"]
                y_label = "Index of Exercise (0-100)"

            for metric in metrics:
                fig = px.bar(filtered_player_data, x="Date", y=metric, title=f"Hip Strength in {metric}")
                fig = add_average_lines(fig, metric)
                injury.plotly_chart(fig, use_container_width=True)

        elif injury_perspective == "Shoulder-Strength":
            if absVals:
                metrics = ["SH Int L", "SH Int R", "SH Ext L", "SH Ext R"]
                y_label = "Newton"
            else:
                metrics = ["SH Int L_index", "SH Int R_index", "SH Ext L_index", "SH Ext R_index"]
                y_label = "Index of Exercise (0-100)"

            for metric in metrics:
                fig = px.bar(filtered_player_data, x="Date", y=metric, title=f"Shoulder Strength in {metric}")
                fig = add_average_lines(fig, metric)
                injury.plotly_chart(fig, use_container_width=True)
